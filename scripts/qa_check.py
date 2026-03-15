#!/usr/bin/env python3
"""
股票报告 QA 检查脚本
检查 Markdown 格式问题，防止 GitHub Pages 渲染错误
"""
import re
import sys
from pathlib import Path


def check_tables(md_text: str, file_path: str):
    """检查表格格式是否符合 Jekyll/kramdown 要求"""
    errors = []
    lines = md_text.split('\n')
    in_table = False
    table_start_line = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 检测表格行
        if '|' in stripped:
            # 计算 | 的数量（排除转义）
            pipe_count = stripped.count('|')

            if pipe_count >= 2:
                if not in_table:
                    # 表格开始
                    in_table = True
                    table_start_line = i + 1

                    # 检查表格前是否有空行（除非是文件开头或标题后）
                    if i > 0:
                        prev_line = lines[i-1].strip()
                        # 表格前应该是空行、标题、或另一个表格行
                        if prev_line and not prev_line.startswith('#') and not prev_line.startswith('|'):
                            errors.append(f"Line {i+1}: Table should be preceded by blank line (add empty line before table)")

                # 检查分隔行格式
                if re.match(r'^\|[-:\s|]+\|$', stripped):
                    # 这是分隔行，检查格式
                    if not stripped.startswith('|') or not stripped.endswith('|'):
                        errors.append(f"Line {i+1}: Table separator should start and end with |")

                    # 检查是否有至少3个 ---
                    if stripped.count('---') < 2:
                        errors.append(f"Line {i+1}: Table separator should have at least 2 columns (---)")
            else:
                in_table = False
        else:
            if in_table and stripped:
                # 表格结束，检查是否以空行结束
                pass
            in_table = False

    return errors


def check_images(md_text: str, file_path: str):
    """检查图片引用"""
    errors = []
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(img_pattern, md_text)

    for alt, src in matches:
        # 检查本地图片是否存在
        if not src.startswith('http://') and not src.startswith('https://'):
            report_dir = Path(file_path).parent
            img_path = (report_dir / src).resolve()
            if not img_path.exists():
                errors.append(f"Missing local image: {src}")

        # 检查 HTML 文件被当作图片
        if src.endswith('.html'):
            errors.append(f"HTML file used as image (should be link): {src}")

    return errors


def check_links(md_text: str, file_path: str):
    """检查链接格式"""
    errors = []

    # 检查相对路径格式
    if '](charts/' in md_text:
        errors.append("Found '](charts/' - should be '](../charts/' for reports in subdir")

    return errors


def check_structure(md_text: str, file_path: str):
    """检查文档结构"""
    errors = []

    # 检查是否有 H1 标题
    if not re.search(r'^# ', md_text, re.MULTILINE):
        errors.append("Missing H1 title (# Title)")

    # 检查是否有连续的空行（超过2个）
    if re.search(r'\n\n\n\n', md_text):
        errors.append("Excessive blank lines (more than 2 consecutive)")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: qa_check.py <report.md>")
        sys.exit(2)

    report_path = Path(sys.argv[1])
    if not report_path.exists():
        print(f"Report not found: {report_path}")
        sys.exit(2)

    md_text = report_path.read_text(encoding='utf-8')

    all_errors = []
    all_errors.extend(check_structure(md_text, str(report_path)))
    all_errors.extend(check_tables(md_text, str(report_path)))
    all_errors.extend(check_images(md_text, str(report_path)))
    all_errors.extend(check_links(md_text, str(report_path)))

    print(f"QA Check: {report_path}")
    print("-" * 40)

    if all_errors:
        print(f"FAILED ({len(all_errors)} issues):")
        for e in all_errors:
            print(f"  ❌ {e}")
        sys.exit(1)
    else:
        print("✅ PASS - All checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
