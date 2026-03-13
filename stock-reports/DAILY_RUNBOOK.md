# Daily Stock Report Runbook

## Purpose
Produce and publish the daily stock reports with **real candlestick charts** to GitHub Pages.

- Repo: `https://github.com/sammyliu459/stock-reports`
- Site: `https://sammyliu459.github.io/stock-reports/`
- Local repo: `/tmp/stock-reports/`
- Reports dir: `/tmp/stock-reports/reports/`
- Charts dir: `/tmp/stock-reports/charts/YYYY-MM-DD/`
- Telegram group/topic (stock reports): `-1003862869671` / topic `45`

---

## Schedule (America/Los_Angeles)
- **Morning report** by ~9:00 AM: `YYYY-MM-DD-morning-report.md`
- **Afternoon report** by ~3:00 PM: `YYYY-MM-DD-afternoon-report.md`

---

## Execution Model
Use a **sub-agent** for execution (multi-step, safer isolation). Main session handles approvals/status updates.

---

## Step-by-Step Checklist

### 1) Prep & Sync
- [ ] `cd /tmp/stock-reports`
- [ ] `git pull origin main`
- [ ] Confirm branch is correct and clean enough to proceed (`git status`)
- [ ] Compute `TODAY=$(date +%F)`

### 2) Gather Market Inputs
- [ ] Capture broad market context (SPY/QQQ/IWM, yields, dollar, major macro headlines)
- [ ] Check earnings/catalysts relevant for today
- [ ] Build shortlist of tickers to include (focus on catalyst + volume + price action)

### 3) X/Twitter Signal Pass (Bird)
- [ ] Verify auth: `bird check`
- [ ] Use `bird search` for unusual volume/chatter and ticker narratives
- [ ] Extract top sentiment shifts and notable ticker mentions
- [ ] Cross-check at least key claims with reliable web sources when possible

### 4) Fetch Real Candlestick Charts
- [ ] Create folder: `/tmp/stock-reports/charts/$TODAY/`
- [ ] Download chart images from real sources (TradingView / Yahoo Finance / StockCharts)
- [ ] Use deterministic filenames (example: `$TICKER-daily.png`, `$TICKER-1h.png`)
- [ ] Verify each file opens and is from today’s session context

### 5) Draft the Report Markdown
- [ ] Create target file in `/tmp/stock-reports/reports/`:
  - Morning: `$TODAY-morning-report.md`
  - Afternoon: `$TODAY-afternoon-report.md`
- [ ] Include:
  - [ ] Market overview (regime + key drivers)
  - [ ] Top opportunities / risks
  - [ ] Ticker-by-ticker notes
  - [ ] Embedded chart links to local `charts/$TODAY/...`
  - [ ] Brief action bias (bullish/neutral/bearish + what invalidates it)

### 6) QA Pass (Hard Gate)
- [ ] Date and timezone labels are correct (PST/PDT)
- [ ] No stale charts from prior dates
- [ ] All image links render in markdown preview
- [ ] Numbers/claims sanity-checked
- [ ] Tone is concise and non-hype

### 7) Publish to GitHub
- [ ] Update `README.md` with new report links at the top of the table.
- [ ] `git add reports/ charts/ README.md`
- [ ] `git commit -m "Add report with charts for $TODAY"`
- [ ] `git push origin main`

### 8) Verify Website
- [ ] Open `https://sammyliu459.github.io/stock-reports/`
- [ ] Confirm new report appears and charts load
- [ ] If not updated yet, wait a short interval and refresh

### 9) Notify Telegram (Stock Topic)
- [ ] Send concise update to group `-1003862869671`, topic `45`
- [ ] Include direct report link and 1–2 key takeaways

### 10) Log Ops Notes
- [ ] Record issues/fixes (source blocked, chart path break, timing delays)
- [ ] Add persistent lessons to memory/docs so next run is smoother

---

## Report Skeleton (Quick Template)

```md
# {DATE} {Morning|Afternoon} Stock Report

## Market Overview
- Regime:
- Key drivers:
- Risk flags:

## High-Priority Setups
1. **$TICKER**
   - Thesis:
   - Catalyst:
   - Risk:
   - Bias:
   - Invalidation:
   - Chart: ![](../charts/{DATE}/{TICKER}-daily.png)

## Watchlist / What Changed Today
- 

## Bottom Line
- 
```

---

## Failure / Recovery Playbook
- If chart source fails:
  - [ ] Try alternate source (Yahoo ↔ TradingView ↔ StockCharts)
  - [ ] Keep naming convention unchanged
- If push fails:
  - [ ] `git status`, resolve conflicts, retry push
- If Pages stale:
  - [ ] Confirm push landed on `main`, then re-check after delay
- If Bird auth fails:
  - [ ] `bird check`, refresh logged-in browser session, retry

---

## Non-Negotiables
- Use **real downloaded charts**, never fabricated images.
- Don’t publish without QA.
- Prefer concise, evidence-based commentary over hype.
- Use sub-agent execution for full runs.
