# Stock Research Agent - 股票研究报告代理

## 任务目标
生成每日股票研究报告，包含：
1. 市场情绪分析（Twitter/X 数据）
2. 异常波动股票识别
3. **黄金/白银比率** (实时计算并追踪)
4. **真实K线图**（使用 QuickChart API 生成真实图表）
5. 中文总结报告

## 工作流程

### 1. 搜索热门股票和话题
使用 `bird` skill 搜索：
- "stock market trends"
- "unusual volume stocks"
- "$TICKER options flow"
- "gold silver ratio"
- "gold price" / "silver price"
- "Fear and Greed Index"
- "VIX"

### 2. 计算黄金/白银比率
每次报告必须包含：

**获取价格数据**:
- 使用 `web_fetch` 访问 https://finance.yahoo.com/quote/GC%3DF 获取黄金价格
- 使用 `web_fetch` 访问 https://finance.yahoo.com/quote/SI%3DF 获取白银价格
- 或使用 `bird` 搜索 "gold price today" / "silver price today"

**计算公式**:
```
金/银比率 = 黄金价格 / 白银价格
```

**解读参考**:
- 比率 > 80: 白银相对黄金被低估
- 比率 50-70: 正常区间
- 比率 < 30: 白银相对强势，可能接近顶部

### 3. 生成真实K线图 (使用 QuickChart API)

#### 3.1 个股/指数长期图 (日线/周线)
使用 QuickChart API 生成真实K线图：

```bash
# 生成个股周线图 (1-6个月)
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/NVDA_weekly.png \
  "https://quickchart.io/chart?w=800&h=400&c={type:'candlestick',data:{datasets:[{label:'NVDA',data:[...]}]}}"
```

更简单的方法 - 使用 Finviz 图表API (直接下载):
```bash
# Finviz 提供可直接下载的图表
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/NVDA_chart.png \
  "https://finviz.com/chart.ashx?t=NVDA&ty=c&ta=1&p=w&s=l"

# 参数说明:
# t=TICKER, ty=c (candlestick), ta=1 (技术分析), p=w (weekly), s=l (large)
```

#### 3.2 大盘指数 (分时+长期)
```bash
# SPY 日线图
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/SPY_daily.png \
  "https://finviz.com/chart.ashx?t=SPY&ty=c&ta=1&p=d&s=l"

# SPY 周线图
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/SPY_weekly.png \
  "https://finviz.com/chart.ashx?t=SPY&ty=c&ta=1&p=w&s=l"

# QQQ 周线图
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/QQQ_weekly.png \
  "https://finviz.com/chart.ashx?t=QQQ&ty=c&ta=1&p=w&s=l"

# VIX 日线图
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/VIX_daily.png \
  "https://finviz.com/chart.ashx?t=VIX&ty=c&ta=1&p=d&s=l"
```

#### 3.3 黄金/白银长期图
```bash
# 黄金周线图 (GC=F 是黄金期货代码)
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/GOLD_weekly.png \
  "https://finviz.com/chart.ashx?t=GC%3DF&ty=c&ta=1&p=w&s=l"

# 白银周线图 (SI=F 是白银期货代码)
curl -o /tmp/stock-reports/charts/YYYY-MM-DD/SILVER_weekly.png \
  "https://finviz.com/chart.ashx?t=SI%3DF&ty=c&ta=1&p=w&s=l"
```

#### 3.4 金/银比率图
由于 Finviz 不支持比率直接绘图，使用文字描述 + 历史数据表格：
```markdown
### 金/银比率历史走势
| 日期 | 比率 | 趋势 |
|------|------|------|
| ... | ... | ... |
```
或搜索网络上的比率图表链接。

### 图表分层策略 (严格执行)

| 对象 | 图表类型 | 来源 | 命令示例 |
|------|----------|------|----------|
| **个股** | 只用周线图 | Finviz | `curl -o TICKER_weekly.png "https://finviz.com/chart.ashx?t=TICKER&ty=c&ta=1&p=w&s=l"` |
| **大盘指数** | 日线图+周线图 | Finviz | `curl -o SPY_daily.png "https://finviz.com/chart.ashx?t=SPY&ty=c&ta=1&p=d&s=l"` |
| **黄金/白银** | 周线图 | Finviz | `curl -o GOLD_weekly.png "https://finviz.com/chart.ashx?t=GC%3DF&ty=c&ta=1&p=w&s=l"` |
| **金/银比率** | 历史数据表 | 计算 | 手动计算并制作表格 |

**禁止**: 个股使用分时图/5分钟图（无意义）

### 4. 生成报告

报告结构:
```markdown
# 股票研究报告 - YYYY-MM-DD

## 📊 市场概览
- Fear & Greed Index: [value]
- VIX: [value]

![SPY 日线图](./charts/YYYY-MM-DD/SPY_daily.png)
![SPY 周线图](./charts/YYYY-MM-DD/SPY_weekly.png)

## 🥇 黄金/白银比率分析
**当前比率**: [XX.XX]
- 黄金: $[XXXX]
- 白银: $[XX]

![黄金周线图](./charts/YYYY-MM-DD/GOLD_weekly.png)
![白银周线图](./charts/YYYY-MM-DD/SILVER_weekly.png)

### 历史比率参考
| 时期 | 比率 | 说明 |
|------|------|------|
| 2020年3月 | ~125 | COVID恐慌高点 |
| 2011年4月 | ~32 | 银疯狂低点 |
| 长期平均 | ~55 | 历史均值 |
| 当前 | [XX] | 当前位置 |

## 🔥 热门股票分析

### [TICKER] - [Name]
**价格**: $[price] ([change]%)

![周线图](./charts/YYYY-MM-DD/TICKER_weekly.png)
*注: 周线图展示长期趋势，含MA20/50/200均线*

**分析**:
- [要点1]
- [要点2]

## 📈 策略建议
- [建议]

---
生成时间: [timestamp]
数据来源: Twitter/X, Finviz, Yahoo Finance
```

### 5. 完整执行脚本示例

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
CHART_DIR="/tmp/stock-reports/charts/$DATE"
REPORT_DIR="/tmp/stock-reports/reports"

mkdir -p "$CHART_DIR"

# 下载大盘图表
curl -sL "https://finviz.com/chart.ashx?t=SPY&ty=c&ta=1&p=d&s=l" -o "$CHART_DIR/SPY_daily.png"
curl -sL "https://finviz.com/chart.ashx?t=SPY&ty=c&ta=1&p=w&s=l" -o "$CHART_DIR/SPY_weekly.png"
curl -sL "https://finviz.com/chart.ashx?t=QQQ&ty=c&ta=1&p=w&s=l" -o "$CHART_DIR/QQQ_weekly.png"
curl -sL "https://finviz.com/chart.ashx?t=VIX&ty=c&ta=1&p=d&s=l" -o "$CHART_DIR/VIX_daily.png"

# 下载贵金属图表
curl -sL "https://finviz.com/chart.ashx?t=GC%3DF&ty=c&ta=1&p=w&s=l" -o "$CHART_DIR/GOLD_weekly.png"
curl -sL "https://finviz.com/chart.ashx?t=SI%3DF&ty=c&ta=1&p=w&s=l" -o "$CHART_DIR/SILVER_weekly.png"

# 下载热门个股图表 (根据 bird 搜索结果)
for TICKER in NVDA TSLA; do
    curl -sL "https://finviz.com/chart.ashx?t=$TICKER&ty=c&ta=1&p=w&s=l" -o "$CHART_DIR/${TICKER}_weekly.png"
done

echo "图表下载完成到 $CHART_DIR"
ls -la "$CHART_DIR"
```

### 6. 推送报告
```bash
cd /tmp/stock-reports
git pull origin main
git add reports/ charts/
git commit -m "Add report with real charts for $DATE"
git push origin main
```

## Finviz 图表参数参考

| 参数 | 值 | 说明 |
|------|-----|------|
| t | TICKER | 股票代码 |
| ty | c | candlestick (K线图) |
| ta | 1 | 显示技术分析指标 |
| p | d/w/m | 周期: daily/weekly/monthly |
| s | l | large 尺寸 (适合网页展示) |

**完整URL格式**:
```
https://finviz.com/chart.ashx?t=[TICKER]&ty=c&ta=1&p=[周期]&s=l
```

## 重要提醒
⚠️ **必须使用真实下载的图表**
- 使用 curl 从 Finviz 下载实际 PNG 图片
- 不要使用外部链接，必须保存到 charts/ 目录
- 个股只用周线图，禁止分时图
- 每个重点股票都必须有对应的图表文件

## 工具使用
- `bird` - Twitter/X搜索热门股票
- `curl` - 下载 Finviz 图表
- `web_fetch` - 获取黄金价格数据
- `exec` - 执行批量下载脚本
