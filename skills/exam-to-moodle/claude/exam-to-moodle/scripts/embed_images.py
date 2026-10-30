#!/usr/bin/env python3
"""Embed images into a Moodle XML file.

Replaces every [[IMAGE:name]] placeholder inside a <text> element with an
<img src="@@PLUGINFILE@@/name"> tag, and adds the image as a base64 <file>
element to the same parent (questiontext, graderinfo, answer, ...), which is
where Moodle expects it.

Usage: python embed_images.py <quiz.xml> --images <work_dir>/images
The file is updated in place. Prints what was embedded or missing.
"""
import argparse
import base64
import os
import re
import sys

from lxml import etree

PLACEHOLDER = re.compile(r"\[\[IMAGE:([^\]]+)\]\]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xml")
    ap.add_argument("--images", required=True)
    args = ap.parse_args()

    parser = etree.XMLParser(strip_cdata=False)
    tree = etree.parse(args.xml, parser)
    embedded, missing = 0, []

    for text_el in tree.iter("text"):
        if not text_el.text or "[[IMAGE:" not in text_el.text:
            continue
        parent = text_el.getparent()
        names = PLACEHOLDER.findall(text_el.text)

        def to_img(m):
            return f'<img src="@@PLUGINFILE@@/{m.group(1)}" alt="" style="max-width:100%">'

        html = PLACEHOLDER.sub(to_img, text_el.text)
        if parent.get("format") is None:
            parent.set("format", "html")
        text_el.text = etree.CDATA(html)
        existing = {f.get("name") for f in parent.findall("file")}
        insert_at = parent.index(text_el) + 1
        for name in names:
            if name in existing:
                continue
            path = os.path.join(args.images, name)
            if not os.path.isfile(path):
                missing.append(name)
                continue
            f = etree.Element("file", name=name, path="/", encoding="base64")
            with open(path, "rb") as fh:
                f.text = base64.b64encode(fh.read()).decode("ascii")
            parent.insert(insert_at, f)
            insert_at += 1
            existing.add(name)
            embedded += 1

    tree.write(args.xml, xml_declaration=True, encoding="UTF-8", pretty_print=True)
    print(f"Embedded {embedded} image(s) into {args.xml}")
    if missing:
        print("MISSING image files: " + ", ".join(missing))
        sys.exit(1)


if __name__ == "__main__":
    main()