#!/bin/bash
# gate_check.sh - Security guard for critical operations
# Purpose: Add context density to deferral requests to prevent blind approval ("rubber-stamping").

OPERATION=$1
CONTEXT=$2

echo "--- SECURITY GATE CHECK ---"
echo "Operation: $OPERATION"
echo "Context: $CONTEXT"
echo "---------------------------"

case "$OPERATION" in
    "rm -rf"|"config.apply"|"git push --force")
        RISK="CRITICAL"
        ;;
    "git push"|"npm install"|"pip install"|"openclaw update")
        RISK="MEDIUM"
        ;;
    *)
        RISK="LOW"
        ;;
esac

echo "Risk Level: $RISK"

if [ "$RISK" == "CRITICAL" ]; then
    echo "🚨 WARNING: This is a high-risk operation."
    echo "Please verify the context carefully before approving."
fi

echo "Awaiting explicit approval..."
