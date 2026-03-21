#!/bin/bash
# 股票报告生成与发布脚本
# 用法: ./scripts/generate_and_publish.sh <morning|afternoon|weekend>

set -e

REPORT_TYPE="$1"
DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

cd "$REPO_DIR"

# 颜色输出
red() { echo -e "\033[31m$*\033[0m"; }
green() { echo -e "\033[32m$*\033[0m"; }
yellow() { echo -e "\033[33m$*\033[0m"; }

# 检查参数
if [[ -z "$REPORT_TYPE" ]]; then
    red "错误: 请指定报告类型"
    echo "用法: $0 <morning|afternoon|weekend>"
    exit 1
fi

case "$REPORT_TYPE" in
    morning)
        FILENAME="${DATE}-morning-report.md"
        ;;
    afternoon)
        FILENAME="${DATE}-afternoon-report.md"
        ;;
    weekend)
        FILENAME="${DATE}-weekend-report.md"
        ;;
    *)
        red "错误: 未知的报告类型: $REPORT_TYPE"
        echo "可选: morning, afternoon, weekend"
        exit 1
        ;;
esac

REPORT_PATH="reports/$FILENAME"

echo "========================================"
echo "股票报告生成与发布"
echo "日期: $DATE"
echo "类型: $REPORT_TYPE"
echo "文件: $REPORT_PATH"
echo "========================================"

# Step 1: 检查金银数据
yellow "\n[1/5] 检查金银数据..."
if [[ -f ".metals.txt" ]]; then
    source ".metals.txt"
    echo "  当前数据: XAU=$XAU, XAG=$XAG (更新于 $UPDATED)"
    
    # 检查是否超过24小时
    TODAY=$(date +%Y-%m-%d)
    if [[ "$UPDATED" != "$TODAY" ]]; then
        yellow "  ⚠️ 金银数据已过期，正在更新..."
        python3 -c "
import yfinance as yf
g = yf.Ticker('GC=F')
s = yf.Ticker('SI=F')
gp = g.fast_info.last_price
sp = s.fast_info.last_price
print(f'XAU={gp:.2f}')
print(f'XAG={sp:.2f}')
print(f'RATIO={gp/sp:.2f}')
print(f'UPDATED=$(date +%Y-%m-%d)')
print('SOURCE=yfinance')
" > ".metals.txt"
        green "  ✅ 金银数据已更新"
    else
        green "  ✅ 金银数据已是最新"
    fi
else
    red "  ❌ .metals.txt 不存在，请先创建"
    exit 1
fi

# Step 2: 生成报告（由调用者完成，这里只检查）
yellow "\n[2/5] 检查报告文件..."
if [[ -f "$REPORT_PATH" ]]; then
    green "  ✅ 报告已存在: $REPORT_PATH"
else
    yellow "  ⚠️ 报告不存在，请先生成报告: $REPORT_PATH"
    echo "  提示: 报告生成后再次运行此脚本完成发布"
    exit 0
fi

# Step 3: QA 检查
yellow "\n[3/5] 运行 QA 检查..."
if python3 scripts/qa_check.py "$REPORT_PATH"; then
    green "  ✅ QA 检查通过"
else
    red "  ❌ QA 检查失败，请修复问题后重试"
    exit 1
fi

# Step 4: 更新 README 索引（关键步骤！）
yellow "\n[4/5] 更新 README 索引..."
python3 scripts/update_readme_index.py
if [[ $? -eq 0 ]]; then
    green "  ✅ README 索引已更新"
else
    red "  ❌ README 索引更新失败"
    exit 1
fi

# Step 5: Git 提交与推送
yellow "\n[5/5] 提交到 GitHub..."
git add reports/ README.md
if git diff --cached --quiet; then
    yellow "  ⚠️ 没有变更需要提交"
else
    git commit -m "Add $REPORT_TYPE report for $DATE"
    git push origin main
    green "  ✅ 已推送到 GitHub"
fi

echo ""
echo "========================================"
green "发布完成！"
echo "报告: https://sammyliu459.github.io/stock-reports/$REPORT_PATH"
echo "首页: https://sammyliu459.github.io/stock-reports/"
echo "========================================"
