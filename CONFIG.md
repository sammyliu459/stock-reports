# Stock Reports - Configuration

This repository contains daily stock market research reports.

## GitHub Pages

Reports are automatically published to GitHub Pages for easy viewing on desktop and mobile.

**URL**: https://sammyliu459.github.io/stock-reports/

## File Naming Convention

- `reports/YYYY-MM-DD-report.md` - Daily stock research reports
- Reports are written in Chinese with Markdown formatting

## How It Works

1. Daily cron job runs at 9:00 AM and 3:00 PM PST
2. Research is conducted using X/Twitter data via `bird` skill
3. Reports are generated and pushed to this repository
4. GitHub Pages automatically renders the markdown for web viewing
