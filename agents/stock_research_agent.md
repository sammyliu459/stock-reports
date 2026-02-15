# Stock Research Agent - 股票研究报告代理

## 任务目标
生成每日股票研究报告，包含：
1. 市场情绪分析（Twitter/X 数据）
2. 异常波动股票识别
3. **真实K线图**（从网上获取，非想象）
4. 中文总结报告

## 工作流程

### 1. 搜索热门股票和话题
使用 `bird` skill 搜索：
- "stock market trends"
- "unusual volume stocks"
- "$TICKER options flow" (热门股票代码)
- "Fear and Greed Index"
- "VIX"

### 2. 获取真实K线图
对于每个重点股票，执行以下步骤：

**Step 2.1: 搜索真实K线图**
```bash
web_search "[STOCK_TICKER] candlestick chart tradingview yahoo finance"
```

**Step 2.2: 获取图表图片**
- 从搜索结果中找到 TradingView、Yahoo Finance、StockCharts 等可靠来源
- 使用 `web_fetch` 或 `browser` 工具获取图表图片URL
- 如果找到图片URL，下载到本地

**Step 2.3: 保存图表**
- 图表保存在 `/tmp/stock-reports/charts/YYYY-MM-DD/`
- 命名格式: `[TICKER]_candlestick.png`
- 在报告中使用相对路径引用: `../charts/YYYY-MM-DD/[TICKER]_candlestick.png`

### 3. 生成报告
报告格式:
```markdown
# 股票研究报告 - YYYY-MM-DD [Morning/Afternoon]

## 📊 市场概览
- Fear & Greed Index: [value]
- VIX: [value]
- 大盘趋势: [summary]

## 🔥 热门股票分析

### [TICKER 1] - [Company Name]
**价格**: $[price] ([change]%)

![K线图](../charts/YYYY-MM-DD/[TICKER]_candlestick.png)

**分析要点**:
- [要点1]
- [要点2]

**Twitter情绪**:
- [情绪总结]

### [TICKER 2] ...

## ⚠️ 异常信号
- [Unusual volume stocks]
- [Options flow anomalies]

## 📈 策略建议
- [总结性建议]

---
生成时间: [timestamp]
数据来源: Twitter/X, TradingView, Yahoo Finance
```

### 4. 推送报告
1. 保存报告: `/tmp/stock-reports/reports/YYYY-MM-DD-[morning/afternoon]-report.md`
2. 确保图表已保存到 `charts/` 目录
3. 推送至GitHub:
   ```bash
   cd /tmp/stock-reports
   git pull origin main
   git add reports/ charts/
   git commit -m "Add report and charts for YYYY-MM-DD"
   git push origin main
   ```

### 5. 发送Telegram通知
使用 `message` 工具:
- action: "send"
- channel: "telegram"
- target: "-1003862869671"
- threadId: "45"
- message: 包含报告摘要 + GitHub网页链接

## 获取K线图的可靠来源

### 来源优先级:
1. **TradingView** - 最专业，图表质量高
   - URL格式: https://www.tradingview.com/chart/?symbol=[EXCHANGE]:[TICKER]
   - 截图或使用他们的嵌入/图片API

2. **Yahoo Finance** - 数据可靠
   - URL格式: https://finance.yahoo.com/quote/[TICKER]/chart

3. **StockCharts.com** - 技术分析专业
   - 提供公开图表图片

4. **Finviz** - 提供迷你图表
   - URL格式: https://finviz.com/quote.ashx?t=[TICKER]

### 图表规范
- 时间周期: 日间交易用1D, 短线用1H, 趋势用1D/1W
- 包含: 蜡烛图 + 成交量
- 技术指标: 至少包含MA20, MA50
- 图片格式: PNG
- 图片宽度: 1200px (适合网页展示)

## 重要提醒
⚠️ **必须使用真实图表**
- 每次搜索并下载真实K线图
- 不要生成或想象图表
- 如果某个股票找不到图表，注明"图表暂不可用"
- 图表必须对应报告当日的数据

## 工具使用
- `bird` - Twitter/X搜索
- `web_search` - 搜索图表和股票信息
- `browser` - 访问TradingView等网站获取图表
- `exec(curl/wget)` - 下载图表图片
- `session_status` - 获取当前日期
