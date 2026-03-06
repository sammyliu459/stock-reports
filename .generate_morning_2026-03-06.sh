#!/usr/bin/env bash
set -euo pipefail
DATE="2026-03-06"
REPORT_DIR="/tmp/stock-reports/reports"
REPORT_PATH="$REPORT_DIR/${DATE}-morning-report.md"
TMP1="$REPORT_DIR/.${DATE}-morning-report.md.tmp"
TMP2="$REPORT_DIR/.${DATE}-morning-report.md.tmp.retry"

is_market_closed() {
  local d="$1"
  local dow
  dow=$(date -d "$d" +%u)
  if [[ "$dow" -ge 6 ]]; then
    return 0
  fi
  case "$d" in
    2026-01-01|2026-01-19|2026-02-16|2026-04-03|2026-05-25|2026-06-19|2026-07-03|2026-09-07|2026-11-26|2026-12-25)
      return 0
      ;;
  esac
  return 1
}

render_closed() {
  cat > "$1" <<EOF
# 每日早间股票研究简讯 - ${DATE}

## 休市提示
今日为周末或美股假日，常规盘前报告暂停。

## 关注要点
- 复盘本周 SPY/QQQ/VIX 结构变化
- 跟踪黄金/白银比率方向
- 等待下一个交易日盘前信号
EOF
}

render_open() {
  read XAU XAG RATIO < <(awk -F= '/XAU/{x=$2}/XAG/{y=$2}/RATIO/{r=$2}END{print x,y,r}' /tmp/stock-reports/.metals.txt)
  cat > "$1" <<EOF
# 每日早间股票研究报告 - ${DATE}

## 市场热点（盘前）
- 美股期货早盘偏谨慎，核心驱动来自 **2月非农数据偏弱 + 原油上行推升通胀担忧**。
- 半导体分化：**NVDA/AMD** 受潜在 AI 芯片出口审批收紧消息影响承压，而 **MRVL** 因AI相关业绩指引走强。
- 利率与波动联动：10Y美债收益率上行、VIX敏感抬头，成长股短线更容易出现高波动。

## 黄金/白银比率
- 黄金（GC=F）: ${XAU}
- 白银（SI=F）: ${XAG}
- 黄金/白银比率: ${RATIO}

解读：金银比维持在 60 上方，说明风险偏好尚未全面修复，盘前更适合“控制仓位 + 等确认”。

## 核心图表（周线，真实K线）
### Ticker: SPY | Period: Weekly
![SPY 周线](../charts/${DATE}/SPY_weekly.svg)
### Ticker: QQQ | Period: Weekly
![QQQ 周线](../charts/${DATE}/QQQ_weekly.svg)
### Ticker: VIX | Period: Weekly
![VIX 周线](../charts/${DATE}/VIX_weekly.svg)
### Ticker: GC=F（黄金） | Period: Weekly
![GC 周线](../charts/${DATE}/GCF_weekly.svg)
### Ticker: SI=F（白银） | Period: Weekly
![SI 周线](../charts/${DATE}/SIF_weekly.svg)

## 热门个股图表（周线，真实K线）
### Ticker: NVDA | Period: Weekly
![NVDA 周线](../charts/${DATE}/NVDA_weekly.svg)
### Ticker: TSLA | Period: Weekly
![TSLA 周线](../charts/${DATE}/TSLA_weekly.svg)
### Ticker: AAPL | Period: Weekly
![AAPL 周线](../charts/${DATE}/AAPL_weekly.svg)
### Ticker: AMD | Period: Weekly
![AMD 周线](../charts/${DATE}/AMD_weekly.svg)
### Ticker: SMCI | Period: Weekly
![SMCI 周线](../charts/${DATE}/SMCI_weekly.svg)

## 信息来源（热点）
- https://www.tipranks.com/news/stock-market-news-today-3-6-26-u-s-stock-futures-fall-on-escalating-iran-conflict-surging-oil-prices
- https://www.investing.com/news/economy-news/us-futures-extend-losses-after-february-nonfarm-payrolls-data-4547004
- https://tokenist.com/nvidia-nvda-stock-falls-premarket-on-proposed-ai-chip-export-restrictions/
EOF
}

validate_file() {
  local p="$1"
  [[ -s "$p" ]] || return 1
  grep -q '^# ' "$p" || return 1
}

atomic_write_once() {
  local tmp="$1"
  if is_market_closed "$DATE"; then
    render_closed "$tmp"
  else
    render_open "$tmp"
  fi
  validate_file "$tmp"
  mv "$tmp" "$REPORT_PATH"
}

if ! atomic_write_once "$TMP1"; then
  rm -f "$TMP1"
  if ! atomic_write_once "$TMP2"; then
    rm -f "$TMP2"
    echo "ATOMIC_WRITE_FAILED" >&2
    exit 11
  fi
fi

echo "REPORT_READY:$REPORT_PATH"
