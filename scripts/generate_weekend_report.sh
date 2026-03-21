#!/usr/bin/env bash
# 生成周末股票简报（带图表）
set -euo pipefail

DATE="$(date +%Y-%m-%d)"
REPORT_DIR="/tmp/stock-reports/reports"
CHART_DIR="/tmp/stock-reports/charts/${DATE}"
REPORT_PATH="${REPORT_DIR}/${DATE}-weekend-brief.md"

# 创建目录
mkdir -p "${CHART_DIR}"

# 股票列表
TICKERS=("SPY" "QQQ" "IWM" "DIA" "GLD" "SLV" "USO" "TLT" "VIX" "NVDA" "AAPL" "TSLA" "MSFT" "GOOGL" "AMZN" "META" "AMD" "AVGO" "MU" "XOM" "OXY" "JPM" "BRK-B")

# 生成 TradingView 嵌入 HTML
generate_chart_html() {
    local ticker="$1"
    local output="$2"

    # 映射到 TradingView 格式
    local tv_symbol=""
    case "$ticker" in
        SPY|QQQ|IWM|DIA|GLD|SLV|USO|TLT|VIX)
            tv_symbol="AMEX:${ticker}"
            ;;
        *)
            tv_symbol="NASDAQ:${ticker}"
            ;;
    esac

    cat > "$output" <<EOF
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>${ticker} Chart</title>
<style>
body { margin: 0; padding: 0; background: #131722; }
#chart { width: 100%; height: 100vh; }
</style>
</head>
<body>
<div id="chart"></div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
new TradingView.widget({
    "container_id": "chart",
    "width": "100%",
    "height": "100%",
    "symbol": "${tv_symbol}",
    "interval": "D",
    "timezone": "America/New_York",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_top_toolbar": true,
    "hide_legend": false,
    "save_image": false,
    "calendar": false,
    "hide_volume": false,
    "support_host": "https://www.tradingview.com"
});
</script>
</body>
</html>
EOF
}

# 下载/生成图表
echo "Generating charts for ${DATE}..."
for ticker in "${TICKERS[@]}"; do
    output="${CHART_DIR}/${ticker}_daily.html"
    if [[ ! -f "$output" ]]; then
        generate_chart_html "$ticker" "$output"
        echo "  Created ${ticker}_daily.html"
    fi
done

echo "Charts ready in ${CHART_DIR}"
echo ""
echo "Next steps:"
echo "1. Generate weekend brief report with chart references"
echo "2. Run: python3 scripts/update_readme_index.py"
echo "3. Commit and push to GitHub"
