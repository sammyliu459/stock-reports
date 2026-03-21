#!/usr/bin/env bash
# 生成 Yahoo Finance 图表图片链接（可直接嵌入 Markdown）
set -euo pipefail

DATE="$(date +%Y-%m-%d)"
REPORT_DIR="/tmp/stock-reports/reports"
CHART_DIR="/tmp/stock-reports/charts/${DATE}"

mkdir -p "${CHART_DIR}"

# 股票列表
TICKERS=("SPY" "QQQ" "IWM" "DIA" "GLD" "SLV" "USO" "TLT" "VIX" "NVDA" "AAPL" "TSLA" "MSFT" "GOOGL" "AMZN" "META" "AMD" "AVGO" "MU" "XOM" "OXY" "JPM" "BRK-B")

echo "Generating Yahoo Finance chart links for ${DATE}..."
echo ""
echo "Copy these into your Markdown report:"
echo ""

for ticker in "${TICKERS[@]}"; do
    # Yahoo Finance 图表 URL（直接图片）
    echo "### ${ticker}"
    echo "![${ticker} Chart](https://chart.yahoo.com/t?s=${ticker}&w=800&h=500)"
    echo ""
done

echo "---"
echo "Alternative: TradingView 静态图（更美观，但可能不稳定）"
for ticker in "${TICKERS[@]}"; do
    echo "![${ticker}](https://www.tradingview.com/x/?symbol=${ticker}&interval=D)"
done
