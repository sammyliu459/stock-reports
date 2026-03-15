# 股票报告生成流程 (Daily Runbook)

## 快速检查清单

生成报告前必须运行：
```bash
python3 scripts/qa_check.py reports/YYYY-MM-DD-*.md
```

## 报告类型

### 1. 早间报告 (Morning Report)
- **时间**: 9:00 AM PST
- **文件名**: `YYYY-MM-DD-morning-report.md`
- **内容**: 市场开盘前简报、隔夜新闻、期货数据

### 2. 下午报告 (Afternoon Report)
- **时间**: 3:00 PM PST (收盘后)
- **文件名**: `YYYY-MM-DD-afternoon-report.md`
- **内容**: 盘后深度分析、个股扫描、技术指标

### 3. 周末简报 (Weekend Brief)
- **时间**: 周六/周日
- **文件名**: `YYYY-MM-DD-weekend-brief.md`
- **内容**: 本周回顾、下周展望

## 图表生成

### 方案 A: Finviz 图片 (推荐)
使用 Finviz 图表 URL 直接嵌入：
```markdown
![SPY](https://charts2.finviz.com/chart.ashx?t=SPY&ty=c&p=d&l=m)
```

参数说明：
- `t=SPY` - 股票代码
- `ty=c` - 蜡烛图
- `p=d` - 日线
- `l=m` - 中等时间范围

### 方案 B: TradingView HTML (备用)
生成 TradingView 嵌入页面，以链接形式提供：
```markdown
[📈 SPY 图表](../charts/YYYY-MM-DD/SPY_daily.html)
```

生成脚本：
```bash
bash scripts/generate_weekend_report.sh
```

## QA 检查

### 自动检查
```bash
# 检查单个报告
python3 scripts/qa_check.py reports/2026-03-15-weekend-brief.md

# 检查所有报告
for f in reports/*.md; do python3 scripts/qa_check.py "$f"; done
```

### 检查项目
- ✅ 表格格式正确（前后有空行）
- ✅ 图片引用正确（本地图片存在，外部 URL 有效）
- ✅ 链接路径正确（`../charts/` 而非 `charts/`）
- ✅ 文档结构完整（有 H1 标题）

## 发布流程

```bash
# 1. 生成/更新报告
# ...

# 2. QA 检查
python3 scripts/qa_check.py reports/YYYY-MM-DD-*.md

# 3. 更新 README 索引
python3 scripts/update_readme_index.py

# 4. 提交到 GitHub
git add reports/ charts/ README.md
git commit -m "Add report for YYYY-MM-DD"
git push origin main

# 5. 验证 (等待 1-2 分钟后)
open https://sammyliu459.github.io/stock-reports/
```

## 常见问题

### 表格不显示
**原因**: Jekyll/kramdown 要求表格前后有空行  
**修复**: 在表格前添加空行

### 图片不显示
**原因**: HTML 文件被当作图片引用  
**修复**: 改为链接形式 `[text](file.html)` 或使用 Finviz 图片 URL

### 链接 404
**原因**: 相对路径错误  
**修复**: reports/ 下的文件使用 `../charts/` 而非 `charts/`

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `scripts/qa_check.py` | QA 检查 |
| `scripts/update_readme_index.py` | 更新 README 索引 |
| `scripts/generate_weekend_report.sh` | 生成 TradingView HTML 图表 |
| `scripts/preflight_check.py` | 预检（旧版，逐步迁移到 qa_check.py） |

## 参考

- GitHub Pages: https://sammyliu459.github.io/stock-reports/
- 仓库: https://github.com/sammyliu459/stock-reports
- Jekyll Kramdown 表格语法: https://kramdown.gettalong.org/syntax.html#tables
