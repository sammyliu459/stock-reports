# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## GitHub Pages - Stock Reports

Daily stock research reports with **real candlestick charts** are published to GitHub Pages for desktop viewing.

- **Repository**: https://github.com/sammyliu459/stock-reports
- **Website**: https://sammyliu459.github.io/stock-reports/
- **Local path**: `/tmp/stock-reports/`
- **Reports directory**: `/tmp/stock-reports/reports/`
- **Charts directory**: `/tmp/stock-reports/charts/YYYY-MM-DD/`

### Report Schedule
- **Morning report** (9:00 AM PST): Twitter summary → `YYYY-MM-DD-morning-report.md`
- **Afternoon report** (3:00 PM PST): Deep research → `YYYY-MM-DD-afternoon-report.md`

### Charts
Reports include **real candlestick charts** sourced from:
- TradingView
- Yahoo Finance
- StockCharts.com

Charts are downloaded (not imagined) and embedded in reports.

### Manual Push (if needed)
```bash
cd /tmp/stock-reports
git pull origin main
git add reports/ charts/
git commit -m "Add report with charts for $(date +%Y-%m-%d)"
git push origin main
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
