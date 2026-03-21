#!/usr/bin/env python3
import re
import sys
from pathlib import Path

BAD_CHARS = {"%", "="}


def find_images(md_text: str):
    return re.findall(r'!\[[^\]]*\]\(([^)]+)\)', md_text)


def check_tables(md_text: str):
    """检查表格格式是否正确"""
    errors = []
    lines = md_text.split('\n')

    for i, line in enumerate(lines):
        # 检测表格行 (以 | 开头或包含 | 的行)
        if '|' in line and not line.strip().startswith('>'):
            # 检查是否是表格行（包含多个 |）
            if line.count('|') >= 2:
                # 检查前一行是否为空行或也是表格行
                if i > 0:
                    prev_line = lines[i-1].strip()
                    # 表格前应该有空行，或者是表格分隔线
                    if prev_line and not prev_line.startswith('|') and not prev_line.startswith('#') and not prev_line.startswith('-'):
                        # 可能是表格开始，检查前一行是否为空
                        if prev_line:
                            errors.append(f"TABLE_FORMAT: Line {i+1} - Table should be preceded by blank line or header")

                # 检查分隔线格式 (|------|)
                if re.match(r'^\|[-:|\s]+\|$', line.strip()):
                    # 确保分隔线有正确的 | 包裹
                    if not line.strip().startswith('|') or not line.strip().endswith('|'):
                        errors.append(f"TABLE_SEPARATOR: Line {i+1} - Separator should start and end with |")

    return errors


def check_report(path: Path):
    text = path.read_text(encoding="utf-8")
    img_links = find_images(text)
    errors = []
    external_images = 0

    # 检查图片
    for link in img_links:
        # 跳过外部 URL
        if link.startswith('http://') or link.startswith('https://'):
            external_images += 1
            continue
        target = (path.parent / link).resolve()
        if not target.exists():
            errors.append(f"MISSING_IMAGE: {link}")
            continue
        name = target.name
        if any(ch in name for ch in BAD_CHARS):
            errors.append(f"BAD_FILENAME: {name} (contains % or =)")

    # 检查路径前缀
    if "](charts/" in text:
        errors.append("BAD_PATH_PREFIX: found '](charts/' (should usually be '](../charts/')")

    # 检查表格格式
    table_errors = check_tables(text)
    errors.extend(table_errors)

    return errors, len(img_links), external_images


def main():
    if len(sys.argv) < 2:
        print("Usage: preflight_check.py <report.md>")
        sys.exit(2)

    report = Path(sys.argv[1])
    if not report.exists():
        print(f"Report not found: {report}")
        sys.exit(2)

    errors, n, external = check_report(report)
    print(f"Checked {report} | local_images={n-external} external_images={external}")
    if errors:
        print("FAILED:")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)

    print("PASS")


if __name__ == "__main__":
    main()
