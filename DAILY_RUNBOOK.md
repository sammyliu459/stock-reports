# 股票报告生成流程 (Daily Runbook)

## 快速检查清单

生成报告前必须运行：
```bash
python3 scripts/qa_check.py reports/YYYY-MM-DD-*.md
```

## ⚠️ 黄金/白银数据源（必须使用）

每次生成报告，**必须**先读取 `/tmp/stock-reports/.metals.txt` 获取金银价格。**禁止自己编数字！**

### 数据格式
```
XAU=4822.90
XAG=75.53
RATIO=63.86
UPDATED=2026-03-18
SOURCE=yfinance
```

### 更新流程
1. 检查 `UPDATED` 日期
2. 如果超过24小时，用 yfinance 重新获取：
```bash
python3 -c "
import yfinance as yf
g = yf.Ticker('GC=F')
s = yf.Ticker('SI=F')
gp = g.fast_info.last_price
sp = s.fast_info.last_price
print(f'XAU={gp:.2f}\nXAG={sp:.2f}\nRATIO={gp/sp:.2f}\nUPDATED=$(date +%Y-%m-%d)\nSOURCE=yfinance')
" > /tmp/stock-reports/.metals.txt
```
3. 报告中引用 `.metals.txt` 的 XAU/XAG/RATIO 值

### 事故教训
- 2026-03-18: morning report 用了错误的黄金价格 ($4867 vs 实际 $4822.90)，因为没有强制使用 `.metals.txt`

## 报告类型与频率

| 类型 | 频率 | 时间 | 文件名 | 内容 |
|------|------|------|--------|------|
| 早间报告 | 工作日 | 9:00 AM PST | `YYYY-MM-DD-morning-report.md` | 开盘前简报、隔夜新闻 |
| 下午报告 | 工作日 | 3:00 PM PST | `YYYY-MM-DD-afternoon-report.md` | 盘后深度分析 |
| 周末报告 | **每周一份** | 周六或周日 | `YYYY-MM-DD-weekend-report.md` | 本周回顾、下周展望 |

**注意**: 周末只生成**一份**报告（周六或周日选一天），避免重复。

## 图表生成

### 方案 A: Finviz URL 嵌入（唯一方案）

直接用 Finviz URL 嵌入报告，**不要下载本地图片**！

```markdown
![SPY](https://charts2.finviz.com/chart.ashx?t=SPY&ty=c&p=d&l=1)
![QQQ](https://charts2.finviz.com/chart.ashx?t=QQQ&ty=c&p=d&l=1)
![GC%3DF](https://charts2.finviz.com/chart.ashx?t=GC%3DF&ty=c&p=d&l=1)
![SI%3DF](https://charts2.finviz.com/chart.ashx?t=SI%3DF&ty=c&p=d&l=1)
![NVDA](https://charts2.finviz.com/chart.ashx?t=NVDA&ty=c&p=d&l=1)
![TSLA](https://charts2.finviz.com/chart.ashx?t=TSLA&ty=c&p=d&l=1)
```

**好处**：实时图片、无路径问题、无本地存储、GitHub Pages 直接渲染

**参数**：`t=代码` `ty=c`蜡烛图 `p=d`日线 `l=1`时间范围

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

## 发布流程（推荐）

使用统一脚本，自动完成 QA 检查、README 更新和 GitHub 推送：

```bash
# 1. 先生成报告（手动或脚本）
# ...

# 2. 一键发布（自动 QA + 更新索引 + Git 推送）
./scripts/generate_and_publish.sh morning    # 早间报告
./scripts/generate_and_publish.sh afternoon  # 下午报告
./scripts/generate_and_publish.sh weekend    # 周末报告
```

**脚本会自动：**
- ✅ 检查并更新金银数据（.metals.txt）
- ✅ QA 检查报告格式
- ✅ **更新 README.md 索引**（防止遗漏）
- ✅ Git add / commit / push

---

## 手动发布流程（备用）

如果不用脚本，**必须**执行以下步骤：

```bash
# 1. 生成/更新报告
# ...

# 2. QA 检查
python3 scripts/qa_check.py reports/YYYY-MM-DD-*.md

# 3. ⚠️ 更新 README 索引（容易遗漏！）
python3 scripts/update_readme_index.py

# 4. 提交到 GitHub
git add reports/ charts/ README.md
git commit -m "Add report for YYYY-MM-DD"
git push origin main

# 5. 验证 (等待 1-2 分钟后)
open https://sammyliu459.github.io/stock-reports/
```

## ⚠️ Telegram 发送格式（必须遵守）

Telegram 不支持 Markdown 表格和图片语法！发送到 Telegram 的消息必须：

1. **用 bullet list 代替表格** ✅ `• 黄金: $4,822` ❌ `| 黄金 | $4,822 |`
2. **不要用 `![img](path)`** — Telegram 显示为纯文本
3. **报告链接用 GitHub Pages HTML**：
   - ✅ `https://sammyliu459.github.io/stock-reports/reports/YYYY-MM-DD-morning-report.html`
   - ❌ `reports/YYYY-MM-DD-morning-report.md`（不可点击，显示源码）
4. **消息格式**：
```
📊 早间报告 2026-03-18
• 黄金: $4,822.90
• 白银: $75.53
• 金银比: 63.86
• SPY: 高位震荡
在线查看: https://sammyliu459.github.io/stock-reports/reports/2026-03-18-morning-report.html
```

**注意**：.md 报告文件本身可以正常使用 markdown 表格和图片（GitHub Pages 渲染用）。

## 常见问题

### 表格不显示
**原因**: Jekyll/kramdown 要求表格前后有空行  
**修复**: 在表格前添加空行

### Telegram 表格变纯文本
**原因**: Telegram 不支持 markdown 表格  
**修复**: Telegram 消息改用 bullet list

### 图片不显示
**原因**: HTML 文件被当作图片引用  
**修复**: 改为链接形式 `[text](file.html)` 或使用 Finviz 图片 URL

### 链接 404
**原因**: 相对路径错误  
**修复**: reports/ 下的文件使用 `../charts/` 而非 `charts/`

### Telegram 链接指向 .md 文件
**原因**: 使用了 GitHub 源文件 URL 而非 Pages URL  
**修复**: 改用 `https://sammyliu459.github.io/stock-reports/reports/YYYY-MM-DD-morning-report.html`

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
