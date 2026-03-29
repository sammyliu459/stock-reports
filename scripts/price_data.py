#!/usr/bin/env python3
"""Fetch price data for stock report watchlist using yfinance.

Returns JSON with price, change%, volume, and history for chart generation.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yfinance as yf

# Watchlist from CONFIG.md
DEFAULT_TICKERS = [
    # Indices
    "SPY", "QQQ", "DIA", "IWM",
    # Gold / Silver
    "GLD", "SLV",
    # Tech megacap
    "NVDA", "TSLA", "AAPL", "AMD", "MSFT", "AMZN", "GOOGL", "META",
    # Rates (Treasury yields)
    "^IRX", "^FVX", "^TNX", "^TYX",
    # Sector ETFs
    "XLF", "XLE", "XLK", "XLI", "XLU", "XLV",
]


def fetch_quotes(tickers):
    """Fetch current quote data for a list of tickers."""
    results = {}
    symbols = " ".join(tickers)
    try:
        data = yf.download(symbols, period="5d", auto_adjust=True, progress=False)
    except Exception as e:
        print(f"Download error: {e}", file=sys.stderr)
        return results

    for ticker in tickers:
        try:
            if len(tickers) == 1:
                close = data["Close"]
                volume = data["Volume"]
                open_ = data["Open"]
                high = data["High"]
                low = data["Low"]
            else:
                close = data["Close"][ticker]
                volume = data["Volume"][ticker]
                open_ = data["Open"][ticker]
                high = data["High"][ticker]
                low = data["Low"][ticker]

            close = close.dropna()
            if len(close) < 2:
                results[ticker] = {"error": "insufficient data"}
                continue

            current = float(close.iloc[-1])
            prev_close = float(close.iloc[-2])
            change_pct = ((current - prev_close) / prev_close) * 100

            hist_close = [float(v) for v in close.tolist()]
            hist_dates = [d.strftime("%m/%d") for d in close.index.tolist()]

            results[ticker] = {
                "price": round(current, 2),
                "prev_close": round(prev_close, 2),
                "change_pct": round(change_pct, 2),
                "volume": int(volume.iloc[-1]) if not volume.empty else 0,
                "day_high": float(high.iloc[-1]) if not high.empty else None,
                "day_low": float(low.iloc[-1]) if not low.empty else None,
                "hist_dates": hist_dates,
                "hist_close": hist_close,
            }
        except Exception as e:
            results[ticker] = {"error": str(e)[:100]}

    return results


def fetch_sentiment():
    """Load latest sentiment scan data."""
    hist_file = Path.home() / ".hermes" / "data" / "sentiment" / "history.json"
    if not hist_file.exists():
        return None
    try:
        history = json.loads(hist_file.read_text())
        if history:
            return history[-1]
    except Exception:
        pass
    return None


def build_divergence_table(quotes, sentiment):
    """Cross-reference sentiment tickers with price action."""
    if not sentiment or not sentiment.get("top_tickers"):
        return []

    ticker_counts = dict(sentiment["top_tickers"])
    divergences = []

    for ticker, mentions in ticker_counts.items():
        entry = {"ticker": ticker, "mentions": mentions}

        if ticker in quotes and "error" not in quotes[ticker]:
            q = quotes[ticker]
            entry["price"] = q["price"]
            entry["change_pct"] = q["change_pct"]
            entry["volume"] = q["volume"]

            if mentions >= 2:
                if q["change_pct"] > 1 and sentiment["market"]["bear_pct"] > 30:
                    entry["signal"] = "caution: bearish sentiment but price up"
                elif q["change_pct"] < -1 and sentiment["market"]["bull_pct"] > 40:
                    entry["signal"] = "watch: bullish sentiment but price down"
                else:
                    entry["signal"] = "aligned"
            else:
                entry["signal"] = "low mention"
        else:
            try:
                t = yf.Ticker(ticker)
                h = t.history(period="5d", auto_adjust=True)
                if len(h) >= 2:
                    cur = float(h["Close"].iloc[-1])
                    prev = float(h["Close"].iloc[-2])
                    entry["price"] = round(cur, 2)
                    entry["change_pct"] = round(((cur - prev) / prev) * 100, 2)
                    entry["signal"] = "aligned"
            except Exception:
                entry["signal"] = "no data"

        divergences.append(entry)

    divergences.sort(key=lambda x: (
        0 if "watch" in x.get("signal", "") or "caution" in x.get("signal", "") else 1,
        -x.get("mentions", 0)
    ))
    return divergences


def main():
    parser = argparse.ArgumentParser(description="Fetch price data for stock reports")
    parser.add_argument("--tickers", nargs="+", default=None, help="Override default ticker list")
    parser.add_argument("--with-sentiment", action="store_true", help="Include sentiment divergence")
    parser.add_argument("--json", action="store_true", help="Raw JSON output")
    args = parser.parse_args()

    tickers = args.tickers or DEFAULT_TICKERS
    quotes = fetch_quotes(tickers)

    output = {"timestamp": datetime.utcnow().isoformat(), "quotes": quotes}

    if args.with_sentiment:
        sentiment = fetch_sentiment()
        output["sentiment"] = sentiment
        output["divergence"] = build_divergence_table(quotes, sentiment)

    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
