#!/usr/bin/env python3
"""Generate price charts for stock reports.

Creates clean, compact chart images using matplotlib.
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {
    "up": "#26a69a",
    "down": "#ef5350",
    "bg": "#1a1a2e",
    "grid": "#2a2a4a",
    "text": "#e0e0e0",
}

TICKER_LABELS = {
    "SPY": "S&P 500", "QQQ": "Nasdaq 100", "DIA": "Dow Jones", "IWM": "Russell 2000",
    "GLD": "Gold ETF", "SLV": "Silver ETF",
    "NVDA": "NVIDIA", "TSLA": "Tesla", "AAPL": "Apple", "AMD": "AMD",
    "MSFT": "Microsoft", "AMZN": "Amazon", "GOOGL": "Alphabet", "META": "Meta",
    "^IRX": "3M Treasury", "^FVX": "5Y Treasury", "^TNX": "10Y Treasury", "^TYX": "30Y Treasury",
    "XLF": "Financials", "XLE": "Energy", "XLK": "Technology",
    "XLI": "Industrials", "XLU": "Utilities", "XLV": "Healthcare",
}


def generate_ticker_chart(ticker, quote, output_dir, days=5):
    if "error" in quote:
        return None
    dates = quote.get("hist_dates", [])
    closes = quote.get("hist_close", [])
    if len(dates) < 2:
        return None

    change_pct = quote.get("change_pct", 0)
    color = COLORS["up"] if change_pct >= 0 else COLORS["down"]

    fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    ax.plot(dates, closes, color=color, linewidth=2, marker="o", markersize=4)
    ax.fill_between(dates, closes, min(closes) - (max(closes) - min(closes)) * 0.1,
                     alpha=0.15, color=color)

    ax.tick_params(colors=COLORS["text"], labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.spines["left"].set_color(COLORS["grid"])
    ax.grid(axis="y", alpha=0.2, color=COLORS["grid"])

    label = TICKER_LABELS.get(ticker, ticker)
    price = quote["price"]
    sign = "+" if change_pct >= 0 else ""
    title = f"{label}  ${price:.2f}  ({sign}{change_pct:.2f}%)"
    ax.set_title(title, color=COLORS["text"], fontsize=11, fontweight="bold", pad=10)

    vol = quote.get("volume", 0)
    if vol:
        vol_str = f"{vol/1e6:.1f}M" if vol > 1e6 else f"{vol/1e3:.0f}K"
        ax.text(0.98, 0.02, f"Vol: {vol_str}", transform=ax.transAxes,
                color=COLORS["text"], fontsize=7, alpha=0.6, ha="right")

    fig.tight_layout()
    safe_ticker = ticker.replace("^", "").replace("=", "")
    outpath = output_dir / f"{safe_ticker}_daily.png"
    fig.savefig(outpath, facecolor=COLORS["bg"], bbox_inches="tight")
    plt.close(fig)
    return str(outpath)


def generate_overview_grid(quotes, output_dir, tickers=None):
    if tickers is None:
        tickers = ["SPY", "QQQ", "DIA", "IWM", "GLD", "SLV", "NVDA", "TSLA"]

    available = [t for t in tickers if t in quotes and "error" not in quotes[t]]
    if not available:
        return None

    n = len(available)
    cols = 4
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(12, 3 * rows), dpi=130)
    fig.patch.set_facecolor(COLORS["bg"])

    if rows == 1:
        axes = [axes]
    axes_flat = [ax for row in axes for ax in (row if cols > 1 else [row])]

    for i, ticker in enumerate(available[:rows * cols]):
        ax = axes_flat[i]
        quote = quotes[ticker]
        dates = quote.get("hist_dates", [])
        closes = quote.get("hist_close", [])
        change_pct = quote.get("change_pct", 0)

        if len(dates) < 2:
            ax.set_visible(False)
            continue

        color = COLORS["up"] if change_pct >= 0 else COLORS["down"]
        ax.set_facecolor(COLORS["bg"])
        ax.plot(dates, closes, color=color, linewidth=1.5, marker="o", markersize=3)
        ax.fill_between(dates, closes, min(closes) - (max(closes) - min(closes)) * 0.15,
                        alpha=0.1, color=color)

        label = TICKER_LABELS.get(ticker, ticker)
        sign = "+" if change_pct >= 0 else ""
        ax.set_title(f"{label} {sign}{change_pct:.1f}%", color=color, fontsize=9, fontweight="bold")

        ax.tick_params(colors=COLORS["text"], labelsize=6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(COLORS["grid"])
        ax.spines["left"].set_color(COLORS["grid"])
        ax.grid(axis="y", alpha=0.15, color=COLORS["grid"])

    for i in range(len(available), rows * cols):
        axes_flat[i].set_visible(False)

    fig.tight_layout()
    outpath = output_dir / "overview_grid.png"
    fig.savefig(outpath, facecolor=COLORS["bg"], bbox_inches="tight")
    plt.close(fig)
    return str(outpath)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate price charts")
    parser.add_argument("--data", required=True, help="JSON data from price_data.py")
    parser.add_argument("--output-dir", default="charts", help="Output directory")
    parser.add_argument("--grid-only", action="store_true", help="Only generate overview grid")
    args = parser.parse_args()

    data = json.loads(Path(args.data).read_text())
    quotes = data.get("quotes", {})
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not args.grid_only:
        for ticker, quote in quotes.items():
            path = generate_ticker_chart(ticker, quote, outdir)
            if path:
                print(f"OK: {path}")

    grid = generate_overview_grid(quotes, outdir)
    if grid:
        print(f"GRID: {grid}")


if __name__ == "__main__":
    main()
