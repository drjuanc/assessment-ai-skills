#!/usr/bin/env python3
"""Validate a Moodle XML question file before import.

Usage: python validate_moodle_xml.py <quiz.xml> [--no-feedback | --ai-feedback]
--no-feedback  check that every feedback element is empty (No feedback option).
--ai-feedback  also check AI feedback: every feedback element ends with the
               disclaimer, and general feedback is 40-120 words (feedback
               wrapped in <div class="doc-feedback"> is exempt).
Exit code 0 = no errors (warnings may remain), 1 = errors found.
"""
import argparse
import re
import sys

from lxml import etree

# MCQ scoring table from SKILL.md: number of correct options -> (each correct, each incorrect)
FRACTIONS = {1: (100, 0), 2: (50, -50), 3: (33.33333, -33.33333), 4: (25, -25), 5: (20, -20)}
RESPONSE_FORMATS = {"editor", "editorfilepicker", "plain", "monospaced", "noinline"}
DISCLAIMER = ("<p><em>AI-generated feedback: this explanation was produced by artificial intelligence "
              "and may contain errors. Check it against your course materials or ask your lecturer.</em></p>")
LEFTOVERS = ("[[CORRECT]]", "[[/CORRECT]]", "[[IMAGE:")


def txt(el, path):
    found = el.find(path)
    return (found.text or "").strip() if found is not None else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xml")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--no-feedback", action="store_true")
    mode.add_argument("--ai-feedback", action="store_true")
    args = ap.parse_args()
    errors, warnings = [], []

    raw = open(args.xml, encoding="utf-8").read()
    if not raw.lstrip().startswith("<?xml"):
        errors.append("File does not start with an XML declaration.")
    for marker in LEFTOVERS:
        if marker in raw:
            errors.append(f"Leftover placeholder {marker} found ({raw.count(marker)}x).")

    try:
        root = etree.fromstring(raw.encode("utf-8"), etree.XMLParser(strip_cdata=False))
    except etree.XMLSyntaxError as e:
        print(f"ERROR: not well-formed XML: {e}")
        sys.exit(1)
    if root.tag != "quiz":
        errors.append("Root element is not <quiz>.")

    questions = root.findall("question")
    if not questions or questions[0].get("type") != "category":
        errors.append("The first question must be a category.")

    names, counts = {}, {}
    for q in questions:
        qtype = q.get("type")
        if qtype == "category":
            continue
        name = txt(q, "name/text") or "(no name)"
        counts[qtype] = counts.get(qtype, 0) + 1
        where = f"{name} [{qtype}]"
        if name in names:
            errors.append(f"{where}: duplicate name.")
        names[name] = True

        qt = q.find("questiontext")
        if qt is None or not txt(q, "questiontext/text"):
            errors.append(f"{where}: empty question text.")
        elif qt.get("format") != "html":
            warnings.append(f"{where}: questiontext format is not html.")
        try:
            if float(txt(q, "defaultgrade")) <= 0:
                errors.append(f"{where}: defaultgrade must be greater than 0.")
        except ValueError:
            errors.append(f"{where}: defaultgrade missing or not a number.")

        for tag in ("correctfeedback", "partiallycorrectfeedback", "incorrectfeedback"):
            if txt(q, f"{tag}/text"):
                errors.append(f"{where}: <{tag}> must be empty.")

        if args.no_feedback:
            if txt(q, "generalfeedback/text"):
                errors.append(f"{where}: general feedback must be empty (--no-feedback).")
            if any(txt(a, "feedback/text") for a in q.findall("answer")):
                errors.append(f"{where}: option feedback must be empty (--no-feedback).")

        if args.ai_feedback:
            gf = txt(q, "generalfeedback/text")
            if not gf:
                warnings.append(f"{where}: no general feedback (withheld or missing).")
            elif 'class="doc-feedback"' not in gf:
                if not gf.endswith(DISCLAIMER):
                    errors.append(f"{where}: general feedback does not end with the AI disclaimer.")
                words = len(re.sub(r"<[^>]+>", " ", gf.replace(DISCLAIMER, "")).split())
                if not 40 <= words <= 120:
                    warnings.append(f"{where}: general feedback is {words} words (aim for 40-120).")
            for a in q.findall("answer"):
                af = txt(a, "feedback/text")
                if af and not af.endswith(DISCLAIMER):
                    errors.append(f"{where}: option feedback does not end with the AI disclaimer.")
                elif not af and gf and qtype == "multichoice":
                    warnings.append(f"{where}: an option has no feedback.")

        if qtype == "multichoice":
            answers = q.findall("answer")
            if len(answers) < 2:
                errors.append(f"{where}: fewer than two answers.")
            fr = []
            for a in answers:
                try:
                    f = float(a.get("fraction"))
                except (TypeError, ValueError):
                    errors.append(f"{where}: answer without a valid fraction.")
                    continue
                fr.append(f)
                atext = (a.findtext("text") or "")
                if re.match(r"^\s*(<p>)?\s*(\(?[A-Ea-e]\)|[A-E]\.|\(?[ivx]+\))\s", atext):
                    warnings.append(f"{where}: option text may still start with a label: {atext[:40]!r}")
            n_correct = sum(1 for f in fr if f > 0)
            expected = FRACTIONS.get(n_correct)
            if expected is None:
                errors.append(f"{where}: {n_correct} correct options; the scoring table covers 1 to 5.")
            else:
                for f in fr:
                    if not any(abs(f - v) < 0.0001 for v in expected):
                        errors.append(f"{where}: fraction {f} does not match the scoring table for "
                                      f"{n_correct} correct option(s) ({expected[0]} correct, {expected[1]} incorrect).")
            single = txt(q, "single")
            if single == "true" and n_correct != 1:
                errors.append(f"{where}: single-answer question needs exactly one correct option.")
            if single == "false" and n_correct < 2:
                errors.append(f"{where}: multiple-response question needs at least two correct options.")

        elif qtype == "matching":
            subs = q.findall("subquestion")
            with_text = [s for s in subs if txt(s, "text")]
            if len(with_text) < 2:
                errors.append(f"{where}: fewer than two subquestions with text.")
            if len(subs) < 3:
                errors.append(f"{where}: fewer than three answers (including distractors).")
            for s in subs:
                if re.search(r"<[a-zA-Z/][^>]*>", s.findtext("answer/text") or ""):
                    errors.append(f"{where}: matching answer contains HTML.")

        elif qtype == "essay":
            rf = txt(q, "responseformat")
            if rf not in RESPONSE_FORMATS:
                errors.append(f"{where}: responseformat '{rf}' is not valid.")
            def num(tag):
                v = txt(q, tag)
                return int(v) if re.fullmatch(r"-?\d+", v) else None
            mn, mx = num("minwordlimit"), num("maxwordlimit")
            if mn is not None and mx is not None and mn >= mx:
                errors.append(f"{where}: minwordlimit is not lower than maxwordlimit.")
            att, req = num("attachments") or 0, num("attachmentsrequired") or 0
            if att != -1 and req > att:
                errors.append(f"{where}: attachmentsrequired exceeds attachments.")
            if rf == "noinline":
                if num("responserequired") != 0:
                    errors.append(f"{where}: upload-only question must have responserequired 0.")
                if req < 1:
                    errors.append(f"{where}: upload-only question must require at least one attachment.")
                if mn is not None or mx is not None:
                    errors.append(f"{where}: upload-only question cannot have word limits.")
            ft = txt(q, "filetypeslist")
            if ft and not all(x.strip().startswith(".") for x in ft.split(",")):
                errors.append(f"{where}: filetypeslist entries must start with a dot.")
        else:
            warnings.append(f"{where}: question type not checked by this script.")

    print("Questions: " + (", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "none"))
    for w in warnings:
        print("WARNING: " + w)
    for e in errors:
        print("ERROR: " + e)
    print("RESULT: " + ("FAIL" if errors else "PASS"))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()