# Stock Reports Skill

Maintains the daily stock reports repo at https://github.com/sammyliu459/stock-reports

## Required Before Posting (Do Not Skip)

Reference mapping: `TICKER-MAPPING.md` (source-specific ticker symbols for Yahoo/TradingView/FRED).

1. **Path normalization**
   - All report image paths must use `../charts/...` (not `charts/...`).
2. **Safe filenames**
   - Never keep `%` or `=` in chart filenames for Pages rendering.
   - Use safe names like `GC_weekly.png`, `SI_weekly.png`.
3. **Preflight check**
   - Run:
   ```bash
   scripts/preflight_check.py reports/YYYY-MM-DD-*.md
   ```
   - Must return `PASS` before posting link.
4. **US Treasury yields required in report body**
   - Include at least: **3M (^IRX), 5Y (^FVX), 10Y (^TNX), 30Y (^TYX)**.
5. **When posting to Telegram, always include direct report links**
   - Include the clickable direct URL to the latest report (e.g., `.../reports/YYYY-MM-DD-afternoon-report.html`).
   - Also include homepage index URL as fallback.

## Common Issues & Fixes

### Issue 1: Charts not showing in reports
**Cause:** Reports use relative paths like `charts/2026-02-17/SPY.png` but reports are in `/reports/` subfolder.

**Fix:**
```bash
sed -i 's|](charts/|](../charts/|g' reports/*.md
```

### Issue 2: Encoded ticker filenames break on Pages
**Cause:** Files generated as `GC%3DF_weekly.png` / `SI%3DF_weekly.png` (or mixed `%` / `=` variants).

**Fix:** Rename to safe names and update report links.
```bash
mv charts/YYYY-MM-DD/GC%3DF_weekly.png charts/YYYY-MM-DD/GC_weekly.png
mv charts/YYYY-MM-DD/SI%3DF_weekly.png charts/YYYY-MM-DD/SI_weekly.png
# then replace links in report markdown
```

### Issue 3: README table missing latest report
**Cause:** README not regenerated.

**Fix:** Regenerate report table and commit README.

## Repo Structure
- `/reports/` - Markdown reports
- `/charts/` - Chart images organized by date
- `/scripts/preflight_check.py` - Pre-publish validator
- `README.md` - Homepage with reports table

## Commands
```bash
# Clone/pull
git clone https://github.com/sammyliu459/stock-reports.git /tmp/stock-reports
cd /tmp/stock-reports && git pull origin main

# Run preflight
scripts/preflight_check.py reports/2026-02-28-morning-report.md

# Commit/push
git add -A && git commit -m "Fix report links + validation" && git push origin main
```
