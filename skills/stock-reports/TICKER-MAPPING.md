# Ticker Mapping (Cross-Source)

Use this mapping when generating stock reports. Different providers use different symbols.

## US Treasury Yields

| Instrument | Yahoo Finance | TradingView | FRED | Investing.com (common) |
|---|---|---|---|---|
| US 3M | `^IRX` | `TVC:US03MY` (or `US03M`) | `DGS3MO` | US 3 Month |
| US 5Y | `^FVX` | `TVC:US05Y` | `DGS5` | US 5 Year |
| US 10Y | `^TNX` | `TVC:US10Y` | `DGS10` | US 10 Year |
| US 30Y | `^TYX` | `TVC:US30Y` | `DGS30` | US 30 Year |

> Note: Yahoo `^TNX` is yield x10 convention in display context on some platforms. In yfinance downloads, use value as returned by Yahoo for consistency across reports.

## Gold / Silver

| Asset | Yahoo Finance | TradingView | Common spot aliases |
|---|---|---|---|
| Gold futures | `GC=F` | `COMEX:GC1!` | XAUUSD (spot) |
| Silver futures | `SI=F` | `COMEX:SI1!` | XAGUSD (spot) |
| Gold ETF | `GLD` | `AMEX:GLD` | - |
| Silver ETF | `SLV` | `AMEX:SLV` | - |

## Rules for Reports

1. Always fetch treasury yields with Yahoo symbols: `^IRX`, `^FVX`, `^TNX`, `^TYX`.
2. Always fetch metals with Yahoo symbols: `GC=F`, `SI=F`.
3. Chart filenames must be normalized (safe):
   - `GC=F` -> `GC_weekly.png`
   - `SI=F` -> `SI_weekly.png`
4. If a required ticker returns empty data, fail report preflight and do not publish silently.
