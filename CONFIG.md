# Stock Reports Configuration

Single source of truth for report generation parameters.

## Chart Tickers

- SPY: S&P 500
- QQQ: Nasdaq 100
- GLD: Gold ETF (use instead of GC=F)
- SLV: Silver ETF (use instead of SI=F)
- NVDA: NVIDIA
- TSLA: Tesla
- AAPL: Apple
- AMD: AMD
- MSFT: Microsoft
- AMZN: Amazon
- GOOGL: Alphabet
- META: Meta

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

## Banned Patterns

The following will cause validation failures:
- `GC=F` or `GC%3DF` (gold futures)
- `SI=F` or `SI%3DF` (silver futures)
- `CL=F` or `CL%3DF` (crude oil futures)
- `NG=F` or `NG%3DF` (natural gas futures)

## Last Updated

2026-03-20 - Fixed gold/silver tickers from GC=F/SI=F to GLD/SLV
