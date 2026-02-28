#!/usr/bin/env python3
import re
import sys
from pathlib import Path

BAD_CHARS = {"%", "="}


def find_images(md_text: str):
    return re.findall(r'!\[[^\]]*\]\(([^)]+)\)', md_text)


def check_report(path: Path):
    text = path.read_text(encoding="utf-8")
    img_links = find_images(text)
    errors = []

    for link in img_links:
        target = (path.parent / link).resolve()
        if not target.exists():
            errors.append(f"MISSING_IMAGE: {link}")
            continue
        name = target.name
        if any(ch in name for ch in BAD_CHARS):
            errors.append(f"BAD_FILENAME: {name} (contains % or =)")

    if "](charts/" in text:
        errors.append("BAD_PATH_PREFIX: found '](charts/' (should usually be '](../charts/')")

    return errors, len(img_links)


def main():
    if len(sys.argv) < 2:
        print("Usage: preflight_check.py <report.md>")
        sys.exit(2)

    report = Path(sys.argv[1])
    if not report.exists():
        print(f"Report not found: {report}")
        sys.exit(2)

    errors, n = check_report(report)
    print(f"Checked {report} | images={n}")
    if errors:
        print("FAILED:")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)

    print("PASS")


if __name__ == "__main__":
    main()
