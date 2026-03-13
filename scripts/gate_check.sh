#!/bin/bash
# gate_check.sh - Security Gate for Sammy Evolution Blueprint
# Based on Jason Zuo's "Gate System" logic (2026-02-25)

ACTION=$1
TARGET=$2

usage() {
    echo "Usage: $0 <action> <target>"
    echo "Actions: corefile, script, publish, trade"
    exit 1
}

LOG_FILE="/home/dimfox/.openclaw/workspace/memory/gate_check.log"

log_check() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ACTION=$ACTION TARGET=$TARGET RESULT=$1" >> "$LOG_FILE"
}

if [ -z "$ACTION" ]; then usage; fi

case $ACTION in
    corefile)
        echo "[Gate Check] Modifying core config: $TARGET"
        echo "1. Is this change reversible? (Check backups)"
        echo "2. Does the human know about this change?"
        echo "3. Is there a safer way to achieve this?"
        log_check "PENDING_CONFIRMATION"
        # Placeholder for interactive confirmation or logged warning
        exit 0
        ;;
    script)
        echo "[Gate Check] Auditing new script: $TARGET"
        if grep -qE "rm -rf|curl.*\|.*sh|wget.*\|.*sh|chmod 777" "$TARGET"; then
            echo "FAILED: Dangerous patterns detected in $TARGET"
            log_check "FAILED_AUDIT"
            exit 1
        fi
        echo "PASSED: Script $TARGET looks safe."
        log_check "PASSED_AUDIT"
        exit 0
        ;;
    publish)
        echo "[Gate Check] Content Checklist: $TARGET"
        # Check for placeholder leaks or sensitive keys
        if grep -qE "AI_KEY|CREDENTIALS|PASSWORD" "$TARGET"; then
            echo "FAILED: Potential credential leak in $TARGET"
            log_check "FAILED_LEAK_CHECK"
            exit 1
        fi
        echo "PASSED: Content check successful."
        log_check "PASSED_LEAK_CHECK"
        exit 0
        ;;
    trade)
        echo "[Gate Check] Trading Logic Change: $TARGET"
        echo "STOP: Any change to trading logic REQUIRES manual user confirmation."
        log_check "BLOCKED_TRADE_CHANGE"
        exit 1
        ;;
    *)
        usage
        ;;
esac
