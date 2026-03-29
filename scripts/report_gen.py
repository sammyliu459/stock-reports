#!/usr/bin/env python3
"""Generate merged stock report with price data, charts, and sentiment.

Usage:
  python3 report_gen.py --date 2026-03-29 --period morning
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from price_data import fetch_quotes, fetch_sentiment, build_divergence_table, DEFAULT_TICKERS
from chart_gen import generate_ticker_chart, generate_overview_grid


def fmt_volume(vol):
    if not vol:
        return "N/A"
    if vol >= 1e9:
        return f"{vol/1e9:.1f}B"
    if vol >= 1e6:
        return f"{vol/1e6:.1f}M"
    return f"{vol/1e3:.0f}K"


def fmt_change(pct):
    sign = "+" if pct >= 0 else ""
    color = "🟢" if pct >= 0 else "🔴"
    return f"{color} {sign}{pct:.2f}%"


def generate_report(date_str, period, output_dir):
    now = datetime.utcnow()
    chart_dir = REPO_DIR / "charts" / date_str
    chart_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching price data...", file=sys.stderr)
    quotes = fetch_quotes(DEFAULT_TICKERS)

    print(f"Fetching sentiment...", file=sys.stderr)
    sentiment = fetch_sentiment()
    divergences = build_divergence_table(quotes, sentiment) if sentiment else []

    print(f"Generating charts...", file=sys.stderr)
    chart_paths = {}
    for ticker, quote in quotes.items():
        path = generate_ticker_chart(ticker, quote, chart_dir)
        if path:
            chart_paths[ticker] = Path(path).name

    grid_path = generate_overview_grid(quotes, chart_dir)

    period_label = "每日Morning" if period == "morning" else "每日Afternoon"

    lines = []
    lines.append(f"# {period_label}股票研究报告\n")
    lines.append(f"**日期:** {date_str}")
    lines.append(f"**时间:** {now.strftime('%I:%M %p')} UTC")
    lines.append(f"**生成:** 自动合并价格+情绪数据\n")

    # Market Overview Grid
    lines.append("## 市场总览\n")
    if grid_path:
        lines.append(f"![市场总览](../charts/{date_str}/{Path(grid_path).name})\n")

    # Index & Price Table
    lines.append("## 指数与主要ETF\n")
    lines.append("| 标的 | 价格 | 涨跌% | 成交量 |")
    lines.append("|------|------|-------|--------|")
    for t in ["SPY", "QQQ", "DIA", "IWM", "GLD", "SLV"]:
        q = quotes.get(t, {})
        if "error" in q:
            lines.append(f"| {t} | N/A | N/A | N/A |")
            continue
        lines.append(f"| {t} | ${q['price']:.2f} | {fmt_change(q['change_pct'])} | {fmt_volume(q['volume'])} |")
    lines.append("")

    # Treasury Yields
    yield_tickers = ["^IRX", "^FVX", "^TNX", "^TYX"]
    yield_labels = ["3M", "5Y", "10Y", "30Y"]
    lines.append("## 美国国债收益率\n")
    lines.append("| 期限 | 收益率 | 变动 |")
    lines.append("|------|--------|------|")
    for t, label in zip(yield_tickers, yield_labels):
        q = quotes.get(t, {})
        if "error" in q:
            lines.append(f"| {label} | N/A | N/A |")
            continue
        sign = "+" if q["change_pct"] >= 0 else ""
        lines.append(f"| {label} | {q['price']:.2f}% | {sign}{q['change_pct']:.2f}% |")
    lines.append("")

    # Tech Megacap
    lines.append("## 科技巨头\n")
    tech_tickers = ["NVDA", "TSLA", "AAPL", "AMD", "MSFT", "AMZN", "GOOGL", "META"]
    lines.append("| 标的 | 价格 | 涨跌% | 成交量 | 走势图 |")
    lines.append("|------|------|-------|--------|--------|")
    for t in tech_tickers:
        q = quotes.get(t, {})
        if "error" in q:
            lines.append(f"| {t} | N/A | N/A | N/A | - |")
            continue
        chart_link = ""
        if t in chart_paths:
            chart_link = f"[📊](../charts/{date_str}/{chart_paths[t]})"
        lines.append(f"| {t} | ${q['price']:.2f} | {fmt_change(q['change_pct'])} | {fmt_volume(q['volume'])} | {chart_link} |")
    lines.append("")

    # Sector ETFs
    lines.append("## 板块ETF\n")
    sector_tickers = ["XLF", "XLE", "XLK", "XLI", "XLU", "XLV"]
    sector_labels = ["金融", "能源", "科技", "工业", "公用事业", "医疗"]
    lines.append("| 板块 | ETF | 价格 | 涨跌% |")
    lines.append("|------|-----|------|-------|")
    for t, label in zip(sector_tickers, sector_labels):
        q = quotes.get(t, {})
        if "error" in q:
            lines.append(f"| {label} | {t} | N/A | N/A |")
            continue
        lines.append(f"| {label} | {t} | ${q['price']:.2f} | {fmt_change(q['change_pct'])} |")
    lines.append("")

    # Sentiment
    if sentiment:
        mkt = sentiment.get("market", {})
        lines.append("## Twitter/X 市场情绪\n")
        lines.append(f"- 总推文: {mkt.get('total_tweets', 0)}")
        lines.append(f"- 看涨: {mkt.get('bull_pct', 0)}% | 看跌: {mkt.get('bear_pct', 0)}%")
        lines.append(f"- 平均分数: {mkt.get('avg_score', 0)}/5")
        lines.append("")

        if divergences:
            lines.append("## 情绪-价格背离分析\n")
            lines.append("| 股票 | 提及次数 | 价格 | 涨跌% | 信号 |")
            lines.append("|------|---------|------|-------|------|")
            for d in divergences[:15]:
                price_str = f"${d.get('price', 'N/A')}" if d.get('price') else "N/A"
                chg_str = f"{d.get('change_pct', 'N/A')}%" if d.get('change_pct') is not None else "N/A"
                signal = d.get("signal", "")
                if "watch" in signal:
                    signal = f"⚠️ {signal}"
                elif "caution" in signal:
                    signal = f"🟡 {signal}"
                lines.append(f"| {d['ticker']} | {d['mentions']} | {price_str} | {chg_str} | {signal} |")
            lines.append("")

        top_tweets = sentiment.get("top_tweets", [])[:5]
        if top_tweets:
            lines.append("### 热门推文\n")
            for tw in top_tweets:
                user = tw.get("user", "?")
                text = tw.get("text", "")[:120]
                sent = tw.get("sentiment", "neutral")
                tickers = ", ".join(tw.get("tickers", []))
                emoji = "🟢" if sent == "bullish" else "🔴" if sent == "bearish" else "⚪"
                lines.append(f"- {emoji} **@{user}**: {text}...")
                if tickers:
                    lines.append(f"  相关: {tickers}")
            lines.append("")

    lines.append("---\n")
    lines.append("*本报告由自动化系统生成，价格数据来自Yahoo Finance，情绪数据来自Twitter/X。仅供参考，不构成投资建议。*")

    report_path = REPO_DIR / "reports" / f"{date_str}-{period}-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines))

    # Save raw data
    raw_path = chart_dir / "raw_data.json"
    raw_data = {"timestamp": now.isoformat(), "quotes": quotes,
                "sentiment": sentiment, "divergences": divergences}
    raw_path.write_text(json.dumps(raw_data, indent=2, default=str))

    print(str(report_path))
    return str(report_path)


def main():
    parser = argparse.ArgumentParser(description="Generate merged stock report")
    parser.add_argument("--date", default=None, help="Date YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--period", choices=["morning", "afternoon"], default="morning")
    args = parser.parse_args()

    date_str = args.date or datetime.utcnow().strftime("%Y-%m-%d")
    path = generate_report(date_str, args.period, REPO_DIR / "charts" / date_str)
    print(f"\nReport: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
