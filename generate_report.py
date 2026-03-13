
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime, timedelta

# Setup
charts_dir = "/tmp/stock-reports/charts/2026-03-08"
os.makedirs(charts_dir, exist_ok=True)

symbols = ["SPY", "QQQ", "GLD", "SLV"]

data_dict = {}
for s in symbols:
    df = yf.download(s, period="3mo")
    # Handle MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    # Clean data: dropna and ensure float
    df = df.dropna().astype(float)
    data_dict[s] = df
    # Save chart
    mpf.plot(df.tail(60), type='candle', volume=True, title=f"{s} Candlestick Chart",
             savefig=os.path.join(charts_dir, f"{s}.png"), style='charles')

# Gold/Silver Ratio
gld = data_dict["GLD"]['Close']
slv = data_dict["SLV"]['Close']
ratio = (gld / slv).dropna()
# Create OHLC for ratio
ratio_ohlc = pd.DataFrame({
    'Open': ratio,
    'High': ratio,
    'Low': ratio,
    'Close': ratio
}, index=ratio.index).astype(float)

mpf.plot(ratio_ohlc.tail(60), type='line', title="Gold/Silver Ratio (GLD/SLV)",
         savefig=os.path.join(charts_dir, "GoldSilverRatio.png"), style='charles')

# Basic Stats for the report
summary = f"# Daily Deep Stock Research - 2026-03-08\n\n"
summary += "## Market Overview (Week Ending 2026-03-06)\n\n"

for s in ["SPY", "QQQ"]:
    last_close = float(data_dict[s]['Close'].iloc[-1])
    prev_close = float(data_dict[s]['Close'].iloc[-2])
    change = ((last_close - prev_close) / prev_close) * 100
    summary += f"- **{s}**: ${last_close:.2f} ({change:+.2f}%)\n"

last_ratio = float(ratio.iloc[-1])
prev_ratio = float(ratio.iloc[-2])
ratio_change = ((last_ratio - prev_ratio) / prev_ratio) * 100
summary += f"- **Gold/Silver Ratio**: {last_ratio:.2f} ({ratio_change:+.2f}%)\n\n"

summary += "## Technical Analysis & Charts\n\n"
summary += "### SPY (S&P 500 ETF)\n![SPY](../charts/2026-03-08/SPY.png)\n\n"
summary += "### QQQ (Nasdaq 100 ETF)\n![QQQ](../charts/2026-03-08/QQQ.png)\n\n"
summary += "### Gold/Silver Ratio\n![Gold/Silver Ratio](../charts/2026-03-08/GoldSilverRatio.png)\n\n"

summary += "## Analysis\n"
summary += "The market showed mixed signals leading into the weekend. The Gold/Silver ratio "
if ratio_change > 0:
    summary += "increased, suggesting a more defensive posture from investors as they favor gold's relative stability."
else:
    summary += "decreased, indicating a potential increase in risk appetite or industrial demand expectations for silver."

summary += "\n\n---"

# We use the relative path for the atomic write from the perspective of the main script
# but the script will output to the specific path required.
temp_path = "/tmp/stock-reports/reports/2026-03-08-afternoon-report.md.tmp"
with open(temp_path, "w") as f:
    f.write(summary)

print("Report and charts generated successfully.")
