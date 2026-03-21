#!/usr/bin/env bash
set -euo pipefail

# Task Runner - DRY-CRON Pattern Implementation
# Usage: task_runner.sh <task-id>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$REPO_DIR/CONFIG.md"
TASK_ID="${1:-}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

fail() {
    log "ERROR: $*"
    exit 1
}

# Parse config from CONFIG.md
# Format: key: value (in code blocks)
get_config() {
    local key="$1"
    awk -F': ' "/^$key:/ {print \$2; exit}" "$CONFIG_FILE" 2>/dev/null | tr -d ' '
}

get_config_list() {
    local section="$1"
    local key="$2"
    awk "/^## $section/,/^## / { if (/^$key:/) { sub(/^$key: */, \"\"); print } }" "$CONFIG_FILE" 2>/dev/null
}

validate_config() {
    [[ -f "$CONFIG_FILE" ]] || fail "CONFIG.md not found at $CONFIG_FILE"
    
    # Check for banned patterns (only in actual ticker definitions, not comments)
    # Look for tickers in list format "- TICKER:" or "TICKER: description"
    if grep -E "^- [A-Z]+=" "$CONFIG_FILE" 2>/dev/null | grep -E "GC=F|SI=F|CL=F|NG=F"; then
        fail "CONFIG.md contains banned futures tickers (GC=F, SI=F, etc.)"
    fi
    
    log "Config validation passed"
}

# Generate report using config values
generate_stock_report() {
    local report_type="$1"  # morning or afternoon
    local date_str
    date_str=$(date +%Y-%m-%d)
    
    # Read config
    local chart_base_url
    chart_base_url=$(get_config "chart_base_url")
    [[ -z "$chart_base_url" ]] && chart_base_url="https://charts2.finviz.com/chart.ashx"
    
    # Get ticker list from config
    local tickers
    tickers=$(get_config_list "Chart Tickers" "- ")
    [[ -z "$tickers" ]] && tickers="SPY QQQ GLD SLV NVDA TSLA AAPL AMD MSFT AMZN GOOGL META"
    
    # Read metals data
    local xau="N/A" xag="N/A" ratio="N/A"
    if [[ -f "$REPO_DIR/.metals.txt" ]]; then
        xau=$(awk -F= '/^XAU=/{print $2}' "$REPO_DIR/.metals.txt")
        xag=$(awk -F= '/^XAG=/{print $2}' "$REPO_DIR/.metals.txt")
        ratio=$(awk -F= '/^RATIO=/{print $2}' "$REPO_DIR/.metals.txt")
    fi
    
    # Build report
    local report_path="$REPO_DIR/reports/${date_str}-${report_type}-report.md"
    
    {
        echo "# 每日${report_type}股票研究报告"
        echo ""
        echo "**日期:** ${date_str}"
        echo "**时间:** $(date '+%H:%M %p %Z')"
        echo ""
        echo "## 贵金属市场"
        echo ""
        echo "- **黄金 (GLD):** $${xau:-N/A}"
        echo "- **白银 (SLV):** $${xag:-N/A}"
        echo "- **金银比率:** ${ratio:-N/A}"
        echo ""
        echo "## 大盘指数"
        echo ""
        
        # Generate chart sections for each ticker
        for ticker in $tickers; do
            local name="$ticker"
            case "$ticker" in
                SPY) name="S&P 500" ;;
                QQQ) name="纳斯达克100" ;;
                GLD) name="黄金ETF" ;;
                SLV) name="白银ETF" ;;
                NVDA) name="NVIDIA" ;;
                TSLA) name="Tesla" ;;
                AAPL) name="Apple" ;;
                AMD) name="AMD" ;;
                MSFT) name="Microsoft" ;;
                AMZN) name="Amazon" ;;
                GOOGL) name="Alphabet" ;;
                META) name="Meta" ;;
            esac
            echo "### $name ($ticker)"
            echo "![$ticker](${chart_base_url}?t=${ticker}&ty=c&p=d&l=1)"
            echo ""
        done
        
        echo "---"
        echo ""
        echo "*本报告由自动化系统生成，仅供参考，不构成投资建议。*"
    } > "$report_path"
    
    log "Report generated: $report_path"
    echo "$report_path"
}

run_qa() {
    local report_path="$1"
    
    if [[ -f "$SCRIPT_DIR/qa_check.py" ]]; then
        python3 "$SCRIPT_DIR/qa_check.py" "$report_path" || fail "QA check failed"
    fi
    
    # Additional validation: check for banned patterns in generated report
    if grep -E "GC%3DF|SI%3DF|GC=F|SI=F" "$report_path" 2>/dev/null; then
        fail "Generated report contains banned futures tickers"
    fi
    
    log "QA passed"
}

publish() {
    cd "$REPO_DIR"
    
    git add reports/
    git commit -m "Add $(date +%Y-%m-%d) reports" || true
    git push origin main
    
    log "Published to GitHub"
}

notify_telegram() {
    local report_type="$1"
    local date_str
    date_str=$(date +%Y-%m-%d)
    
    local html_url="https://sammyliu459.github.io/stock-reports/reports/${date_str}-${report_type}-report.html"
    
    # Use openclaw's internal messaging if available, otherwise echo
    log "Notification: $html_url"
}

# Main task handlers
task_stock_morning() {
    log "Starting morning stock report..."
    validate_config
    
    local report_path
    report_path=$(generate_stock_report "morning")
    run_qa "$report_path"
    publish
    notify_telegram "morning"
    
    log "Morning report complete"
}

task_stock_afternoon() {
    log "Starting afternoon stock report..."
    validate_config
    
    # TODO: Add bird search integration here
    
    local report_path
    report_path=$(generate_stock_report "afternoon")
    run_qa "$report_path"
    publish
    notify_telegram "afternoon"
    
    log "Afternoon report complete"
}

# Dispatcher
case "$TASK_ID" in
    stock-morning)
        task_stock_morning
        ;;
    stock-afternoon)
        task_stock_afternoon
        ;;
    *)
        fail "Unknown task: $TASK_ID. See TASKS.md for available tasks."
        ;;
esac
