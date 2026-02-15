# MEMORY.md

## Entities

### Devices

- **Epson Stylus NX420 Printer (Archived)**
  - **type:** Printer
  - **model:** Epson Stylus NX420
  - **network:**
    - **mac_address:** `00:26:AB:13:6D:E4`
    - **assigned_ip:** `192.168.1.154`
    - **gateway:** `192.168.1.254`
  - **status:**
    - **issue:** Unstable connection on modern routers due to DHCP renewal failure.
    - **resolution:** Requires a static IP or DHCP reservation.
    - **proposed_static_ip:** `192.168.1.250`
    - **Note:** Maintenance removed from core tasks per user request.

## Recurring Tasks

### Daily Stock Research
- **Schedule:** Daily via cron at 9:00 AM PST and 3:00 PM PST
- **Method:** Search X/Twitter using `bird` skill for market sentiment, unusual options flow, institutional vs retail activity
- **Charts:** Real candlestick charts from TradingView/Yahoo Finance (not imagined)
- **Delivery:**
  - Telegram group `-1003862869671` topic 45 (summary + link)
  - GitHub Pages: https://sammyliu459.github.io/stock-reports/ (full report with charts)
- **Repository:** https://github.com/sammyliu459/stock-reports
- **Key metrics to track:** Fear & Greed Index, VIX, NVDA earnings dates

## Security Awareness

### ClawdHub/Skills Security (2026-02-10)
- Rufio (AI agent) found credential stealer in ClawdHub skill (1/286 scanned)
- Malicious skills can read `~/.clawdbot/.env` and exfiltrate secrets
- **Best practices:**
  - Never install skills without reading source code
  - Be suspicious of skills requesting API keys or env access
  - Check author reputation when possible
  - See `memory/moltbook-concerns.md` for full details

## Communication Channels

- **Stock reports:** Telegram group `-1003862869671` topic 45
- **Moltbook alerts:** Telegram group `-1003862869671` topic 24
