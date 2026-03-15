#!/usr/bin/env python3
"""
自动更新 README.md 中的报告索引表格
扫描 reports/ 目录，按日期排序生成最新的索引
"""
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPORTS_DIR = Path("reports")
README_PATH = Path("README.md")
MAX_ENTRIES = 20  # 最多显示最近多少天的报告


def parse_report_filename(filename: str):
    """解析报告文件名，提取日期和类型"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md$', filename)
    if not match:
        return None
    date_str, report_type = match.groups()
    return date_str, report_type


def get_report_emoji(report_type: str):
    """根据报告类型返回对应的 emoji"""
    if 'morning' in report_type:
        return '☀️ Morning'
    elif 'afternoon' in report_type:
        return '🌙 Afternoon'
    elif 'weekend' in report_type or 'weekly' in report_type:
        return '🗓️ Weekend'
    else:
        return '📄'


def get_model_from_date(date_str: str):
    """根据日期推断使用的模型（基于历史切换记录）"""
    # 模型切换历史：
    # - 2026-03-06 之前: Gemini-3
    # - 2026-03-09: GPT-5.3 (测试)
    # - 2026-03-08 之后: Kimi-K2.5 (主要)
    date = datetime.strptime(date_str, '%Y-%m-%d')

    if date <= datetime(2026, 3, 6):
        return 'Gemini-3'
    elif date == datetime(2026, 3, 9):
        return 'GPT-5.3'
    else:
        return 'Kimi-K2.5'


def generate_index_table():
    """生成报告索引表格"""
    if not REPORTS_DIR.exists():
        print(f"Reports directory not found: {REPORTS_DIR}")
        sys.exit(1)

    reports_by_date = defaultdict(list)

    for report_file in sorted(REPORTS_DIR.glob('*.md'), reverse=True):
        parsed = parse_report_filename(report_file.name)
        if not parsed:
            continue
        date_str, report_type = parsed
        reports_by_date[date_str].append({
            'type': report_type,
            'emoji_label': get_report_emoji(report_type),
            'path': f'reports/{report_file.name}',
            'model': get_model_from_date(date_str)
        })

    sorted_dates = sorted(reports_by_date.keys(), reverse=True)[:MAX_ENTRIES]

    lines = ['| 日期 | 报告链接 | 模型 |', '|------|----------|------|']

    for date_str in sorted_dates:
        reports = reports_by_date[date_str]
        type_order = {'morning': 0, 'afternoon': 1, 'weekend': 2, 'weekly': 3}
        reports.sort(key=lambda x: type_order.get(next(
            (k for k in type_order if k in x['type']), 'afternoon'), 99))

        links = ' \\| '.join(
            f"[{r['emoji_label']}]({r['path']})" for r in reports
        )
        model = reports[0]['model'] if reports else 'Unknown'
        lines.append(f'| {date_str} | {links} | {model} |')

    return '\n'.join(lines)


def update_readme():
    """更新 README.md 文件"""
    if not README_PATH.exists():
        print(f"README.md not found: {README_PATH}")
        sys.exit(1)

    content = README_PATH.read_text(encoding='utf-8')
    new_table = generate_index_table()

    # 找到 "## 📊 最新报告" 部分，替换其后的表格
    marker = '## 📊 最新报告\n\n'
    if marker not in content:
        print("Could not find '## 📊 最新报告' section in README.md")
        sys.exit(1)

    # 分割内容
    before_marker = content.split(marker)[0] + marker
    after_section = content.split(marker)[1]

    # 找到表格结束位置（下一个 ## 或 --- 或文件结束）
    next_section_match = re.search(r'\n(## |---|\Z)', after_section)
    if next_section_match:
        after_table = after_section[next_section_match.start():]
    else:
        after_table = ''

    # 组合新内容
    new_content = before_marker + new_table + '\n' + after_table

    README_PATH.write_text(new_content, encoding='utf-8')
    print(f"Updated {README_PATH}")
    print(f"Generated {len(new_table.split(chr(10)))} lines of table")


def main():
    update_readme()
    print("README index updated successfully!")


if __name__ == '__main__':
    main()
