# Task Registry

Single source of truth for all automated tasks.

## Stock Reports

| Task ID | Schedule | Config Section | Script | Cron Payload |
|---------|----------|----------------|--------|--------------|
| stock-morning | 0 9 * * * | CONFIG.md#tickers | task_runner.sh stock-morning | `bash /tmp/stock-reports/scripts/task_runner.sh stock-morning` |
| stock-afternoon | 0 15 * * * | CONFIG.md#tickers | task_runner.sh stock-afternoon | `bash /tmp/stock-reports/scripts/task_runner.sh stock-afternoon` |

## Config Schema

Each task references a config section. Configs use simple key=value format for easy parsing.

## Adding New Tasks

1. Add entry to table above
2. Add config section to CONFIG.md
3. Add handler to task_runner.sh
4. Update cron with thin wrapper payload
