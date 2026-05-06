# Stock Reports Configuration

Single source of truth for report generation parameters.

## Chart Tickers

| Asset | Finviz Ticker | Why |
|-------|---------------|-----|
| S&P 500 | SPY | ✅ Reliable |
| Nasdaq 100 | QQQ | ✅ Reliable |
| Gold | GLD | ✅ ETF (futures GC=F rate-limited) |
| Silver | SLV | ✅ ETF (futures SI=F rate-limited) |
| NVIDIA | NVDA | ✅ Reliable |
| Tesla | TSLA | ✅ Reliable |
| Apple | AAPL | ✅ Reliable |
| AMD | AMD | ✅ Reliable |
| Microsoft | MSFT | ✅ Reliable |
| Amazon | AMZN | ✅ Reliable |
| Alphabet | GOOGL | ✅ Reliable |
| Meta | META | ✅ Reliable |

## Template Variables

Reports should use these variables instead of hardcoded values:

- `{{DATE}}` - YYYY-MM-DD format
- `{{TIME}}` - HH:MM AM/PM PST
- `{{CHART_BASE_URL}}` - https://charts2.finviz.com/chart.ashx
- `{{TICKERS}}` - Comma-separated list from above

## Generation Rules

1. **Never use futures tickers** (GC=F, SI=F, CL=F, NG=F) — they get rate-limited
2. **Use ETFs instead** (GLD, SLV, USO, UNG)
3. **Always reference this CONFIG.md** when generating reports
4. **If this file conflicts with instructions**, this file wins

## Last Updated

2026-03-20 - Fixed gold/silver tickers from GC=F/SI=F to GLD/SLV
