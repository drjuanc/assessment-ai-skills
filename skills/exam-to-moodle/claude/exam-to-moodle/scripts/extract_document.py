#!/usr/bin/env python3
"""Extract an exam document (DOCX or PDF) to plain text for Moodle XML conversion.

Red text is wrapped as [[CORRECT]]...[[/CORRECT]], Word list numbering is
written out (A., b), 1.), tables are rendered row by row, and images are saved
and replaced by [[IMAGE:imageN.ext]] placeholders.

Usage: python extract_document.py <input.docx|input.pdf> --out <work_dir>
Writes <work_dir>/document.md and <work_dir>/images/, and prints a summary.
"""
import argparse
import os
import re
import sys

MARK_OPEN, MARK_CLOSE = "[[CORRECT]]", "[[/CORRECT]]"


def is_red_rgb(r, g, b):
    """True for clear reds (FF0000, C00000, E00000 ...), not orange or pink."""
    return r >= 0x99 and g <= 0x66 and b <= 0x66 and r - max(g, b) >= 0x66


# ---------------------------------------------------------------- DOCX
def extract_docx(path, out_dir, stats):
    import docx
    from docx.oxml.ns import qn
    from docx.enum.dml import MSO_COLOR_TYPE

    doc = docx.Document(path)
    img_dir = os.path.join(out_dir, "images")
    numbering = load_numbering(doc, qn)
    counters = {}

    def style_colour(style):
        while style is not None:
            try:
                c = style.font.color
                if c is not None and c.type == MSO_COLOR_TYPE.RGB and c.rgb is not None:
                    return c.rgb
            except Exception:
                pass
            style = style.base_style
        return None

    def run_is_red(run, para):
        c = run.font.color
        if c is not None and c.type is not None:
            if c.type == MSO_COLOR_TYPE.RGB and c.rgb is not None:
                return is_red_rgb(*c.rgb)
            if c.type == MSO_COLOR_TYPE.THEME:
                stats["theme_coloured_runs"] += 1
                return False
        rgb = style_colour(run.style) if run.style is not None else None
        if rgb is None:
            rgb = style_colour(para.style)
        return rgb is not None and is_red_rgb(*rgb)

    def save_images(run_el):
        names = []
        for blip in run_el.iter(qn("a:blip")):
            rid = blip.get(qn("r:embed"))
            part = doc.part.related_parts.get(rid)
            if part is None:
                continue
            os.makedirs(img_dir, exist_ok=True)
            stats["images"] += 1
            ext = os.path.splitext(part.partname)[1] or ".png"
            name = f"image{stats['images']}{ext}"
            with open(os.path.join(img_dir, name), "wb") as fh:
                fh.write(part.blob)
            names.append(f"[[IMAGE:{name}]]")
        return names

    def para_text(para):
        from docx.text.run import Run
        pieces, red_open = [], False
        for child in para._p.iter(qn("w:r")):
            run = Run(child, para)
            images = save_images(child)
            text = run.text
            red = bool(text.strip()) and run_is_red(run, para)
            if red and not red_open:
                pieces.append(MARK_OPEN)
                red_open = True
                stats["red_spans"] += 1
            elif not red and red_open and text.strip():
                pieces.append(MARK_CLOSE)
                red_open = False
            pieces.append(text)
            pieces.extend(images)
        if red_open:
            pieces.append(MARK_CLOSE)
        text = "".join(pieces)
        # tidy: move spaces outside markers, merge adjacent spans
        text = text.replace(MARK_CLOSE + MARK_OPEN, "")
        text = re.sub(r"\[\[CORRECT\]\](\s+)", r"\1[[CORRECT]]", text)
        text = re.sub(r"(\s+)\[\[/CORRECT\]\]", r"[[/CORRECT]]\1", text)
        label = list_label(para, numbering, counters, qn)
        return (label + " " if label else "") + text.strip()

    from docx.text.paragraph import Paragraph
    from docx.table import Table
    lines, table_no = [], 0
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            t = para_text(Paragraph(el, doc))
            if t:
                lines.append(t)
        elif el.tag == qn("w:tbl"):
            table_no += 1
            lines.append(f"[TABLE {table_no}]")
            for row in Table(el, doc).rows:
                cells, seen = [], set()
                for cell in row.cells:
                    if id(cell._tc) in seen:      # horizontally merged cell
                        continue
                    seen.add(id(cell._tc))
                    cells.append(" / ".join(p for p in (para_text(p) for p in cell.paragraphs) if p))
                lines.append("| " + " | ".join(cells) + " |")
            lines.append(f"[/TABLE {table_no}]")
    return "\n".join(lines)


def load_numbering(doc, qn):
    try:
        root = doc.part.numbering_part.element
    except Exception:
        return None
    abstract = {}
    for an in root.findall(qn("w:abstractNum")):
        levels = {}
        for lvl in an.findall(qn("w:lvl")):
            def val(tag, default):
                e = lvl.find(qn(tag))
                return e.get(qn("w:val")) if e is not None else default
            levels[int(lvl.get(qn("w:ilvl")))] = {
                "fmt": val("w:numFmt", "decimal"),
                "text": val("w:lvlText", "%1."),
                "start": int(val("w:start", "1")),
            }
        abstract[an.get(qn("w:abstractNumId"))] = levels
    nums = {}
    for n in root.findall(qn("w:num")):
        a = n.find(qn("w:abstractNumId"))
        if a is not None:
            nums[n.get(qn("w:numId"))] = abstract.get(a.get(qn("w:val")), {})
    return nums


def fmt_number(n, fmt):
    if fmt in ("upperLetter", "lowerLetter"):
        s = ""
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s if fmt == "upperLetter" else s.lower()
    if fmt in ("upperRoman", "lowerRoman"):
        vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
        s = ""
        for v, sym in vals:
            while n >= v:
                s, n = s + sym, n - v
        return s if fmt == "upperRoman" else s.lower()
    if fmt == "bullet":
        return "•"
    return str(n)


def list_label(para, numbering, counters, qn):
    if not numbering:
        return ""
    pPr = para._p.pPr
    numPr = pPr.find(qn("w:numPr")) if pPr is not None else None
    style = para.style
    while numPr is None and style is not None:
        spPr = style.element.pPr
        numPr = spPr.find(qn("w:numPr")) if spPr is not None else None
        style = style.base_style
    if numPr is None:
        return ""
    nid = numPr.find(qn("w:numId"))
    ilvl = numPr.find(qn("w:ilvl"))
    num_id = nid.get(qn("w:val")) if nid is not None else None
    level = int(ilvl.get(qn("w:val"))) if ilvl is not None else 0
    levels = numbering.get(num_id)
    if not levels or level not in levels or num_id == "0":
        return ""
    cnt = counters.setdefault(num_id, {})
    cnt[level] = cnt.get(level, levels[level]["start"] - 1) + 1
    for deeper in [k for k in cnt if k > level]:
        del cnt[deeper]
    if levels[level]["fmt"] == "bullet":
        return "•"
    label = levels[level]["text"]
    for k in range(level + 1):
        if k in levels:
            n = cnt.get(k, levels[k]["start"])
            label = label.replace(f"%{k + 1}", fmt_number(n, levels[k]["fmt"]))
    return label


# ---------------------------------------------------------------- PDF
def pdf_colour_is_red(c):
    if c is None:
        return False
    if isinstance(c, (int, float)):
        return False
    c = list(c)
    if len(c) == 3:
        return is_red_rgb(*(int(v * 255) for v in c))
    if len(c) == 4:                                   # CMYK
        cy, m, y, k = c
        return is_red_rgb(int(255 * (1 - cy) * (1 - k)), int(255 * (1 - m) * (1 - k)), int(255 * (1 - y) * (1 - k)))
    return False


def extract_pdf(path, out_dir, stats):
    import pdfplumber
    lines = []
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, 1):
            stats["images"] += len(page.images)
            if page.images:
                lines.append(f"[PDF IMAGE ON PAGE {page_no}: not extracted; use the Word file to include images]")
            words = page.extract_words(extra_attrs=["non_stroking_color"], keep_blank_chars=False, use_text_flow=True)
            current_top, buf, red_open = None, [], False
            for w in words:
                if current_top is not None and abs(w["top"] - current_top) > 3:
                    if red_open:
                        buf.append(MARK_CLOSE)
                        red_open = False
                    lines.append(" ".join(buf).replace(" " + MARK_CLOSE, MARK_CLOSE).replace(MARK_OPEN + " ", MARK_OPEN))
                    buf = []
                current_top = w["top"]
                red = pdf_colour_is_red(w.get("non_stroking_color"))
                if red and not red_open:
                    buf.append(MARK_OPEN)
                    red_open = True
                    stats["red_spans"] += 1
                elif not red and red_open:
                    buf.append(MARK_CLOSE)
                    red_open = False
                buf.append(w["text"])
            if buf:
                if red_open:
                    buf.append(MARK_CLOSE)
                lines.append(" ".join(buf).replace(" " + MARK_CLOSE, MARK_CLOSE).replace(MARK_OPEN + " ", MARK_OPEN))
            lines.append(f"[END OF PAGE {page_no}]")
    stats["pdf"] = True
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    stats = {"red_spans": 0, "theme_coloured_runs": 0, "images": 0, "existing_markers": 0, "pdf": False}
    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".docx":
        text = extract_docx(args.input, args.out, stats)
    elif ext == ".pdf":
        text = extract_pdf(args.input, args.out, stats)
    else:
        sys.exit("Unsupported file type: use .docx or .pdf (save .doc files as .docx first).")
    stats["existing_markers"] = text.count(MARK_OPEN) - text.count(MARK_CLOSE)
    out_file = os.path.join(args.out, "document.md")
    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(f"Wrote {out_file}")
    print(f"Red spans marked: {stats['red_spans']}")
    print(f"Pre-existing [[CORRECT]] markers without an end marker: {stats['existing_markers']}")
    print(f"Images: {stats['images']}" + (" (saved in images/)" if not stats["pdf"] and stats["images"] else ""))
    if stats["theme_coloured_runs"]:
        print(f"WARNING: {stats['theme_coloured_runs']} runs use theme colours, which were not treated as red. "
              "If answers are missing, ask the user to recolour answers with standard Red.")
    if stats["pdf"]:
        print("NOTE: PDF input. Table layout and list labels are approximate; images are not extracted.")
    if stats["red_spans"] == 0 and stats["existing_markers"] == 0:
        print("WARNING: no red text or markers found.")


if __name__ == "__main__":
    main()