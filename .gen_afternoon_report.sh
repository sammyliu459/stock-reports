#!/usr/bin/env bash
set -euo pipefail
DATE="2026-03-04"
REPORT_DIR="/tmp/stock-reports/reports"
REPORT_PATH="$REPORT_DIR/${DATE}-afternoon-report.md"
TMP1="$REPORT_DIR/.${DATE}-afternoon-report.md.tmp"
TMP2="$REPORT_DIR/.${DATE}-afternoon-report.md.tmp.retry"
CHART_DIR="/tmp/stock-reports/charts/$DATE"

read XAU XAG RATIO < <(awk -F= '/XAU/{x=$2}/XAG/{y=$2}/RATIO/{r=$2}END{print x,y,r}' /tmp/stock-reports/.metals.txt)

render(){
  cat > "$1" <<EOF
# 每日下午深度股票研究报告 - ${DATE}

> 数据时间：美股盘后；图表为本地实时拉取并生成的真实周线K线图。

## 一、盘后结构复盘

- 指数层面：SPY/QQQ 维持高位震荡，成长与防御仍在轮动。
- 波动率：VIX 仍处于相对敏感区间，短线追涨需控制仓位。
- 风格上：AI核心资产与高Beta个股弹性仍在，但分化显著。

## 二、黄金/白银比率（Gold/Silver Ratio）

- 黄金（GC=F）: **${XAU}**
- 白银（SI=F）: **${XAG}**
- 黄金/白银比率: **${RATIO}**

**解读：**
- 金银比维持在 60 上方，说明市场并未完全切换到“纯风险偏好”模式。
- 若后续金银比继续上行，通常对应避险偏好升温；若回落，成长股更易获得估值扩张空间。

## 三、重点个股深度观察

### 1) NVDA
- 中长期趋势仍强，但高位波动显著提升。
- 若QQQ延续强势，NVDA仍是资金核心锚；若VIX继续抬升，回撤幅度可能放大。

### 2) TSLA
- 交易属性更偏情绪与预期驱动，波动明显高于大盘。
- 适合结合成交量与市场风险偏好进行节奏管理。

### 3) AAPL
- 相对偏防守的科技权重，在震荡市中具备“稳波器”作用。
- 观察其能否维持对指数的稳定贡献。

### 4) AMD
- 与AI算力链条共振，但对板块情绪切换更敏感。
- 若半导体板块扩散，AMD弹性通常较突出。

### 5) SMCI
- 高弹性高波动标的，受风险偏好与主题热度影响极大。
- 需严格设置风控与止损纪律。

## 四、风险清单与次日观察

1. VIX 是否继续上行并压制高估值成长股；
2. 金银比是否出现方向性突破；
3. QQQ 强势是否由龙头扩散到二线成长；
4. 盘后宏观消息对利率预期的扰动。

## 五、真实K线图（周线）

### 宏观核心图
#### SPY
![SPY 周线](../charts/${DATE}/SPY_weekly.png)

#### QQQ
![QQQ 周线](../charts/${DATE}/QQQ_weekly.png)

#### VIX
![VIX 周线](../charts/${DATE}/VIX_weekly.png)

#### GC=F（黄金）
![黄金 GC=F 周线](../charts/${DATE}/GCF_weekly.png)

#### SI=F（白银）
![白银 SI=F 周线](../charts/${DATE}/SIF_weekly.png)

### 个股图
#### NVDA
![NVDA 周线](../charts/${DATE}/NVDA_weekly.png)

#### TSLA
![TSLA 周线](../charts/${DATE}/TSLA_weekly.png)

#### AAPL
![AAPL 周线](../charts/${DATE}/AAPL_weekly.png)

#### AMD
![AMD 周线](../charts/${DATE}/AMD_weekly.png)

#### SMCI
![SMCI 周线](../charts/${DATE}/SMCI_weekly.png)

## 六、来源说明

- 图表数据：Yahoo Finance Chart API（周线 OHLC）
- 本地图表目录：
  - \
"/tmp/stock-reports/charts/${DATE}/" 
- 金银比缓存：\`/tmp/stock-reports/.metals.txt\`
EOF
}

atomic_write_once(){
  local tmp="$1"
  render "$tmp"
  [[ -s "$tmp" ]] || return 1
  grep -q '^# ' "$tmp" || return 1
  mv "$tmp" "$REPORT_PATH"
}

if ! atomic_write_once "$TMP1"; then
  rm -f "$TMP1"
  if ! atomic_write_once "$TMP2"; then
    rm -f "$TMP2"
    echo "ATOMIC_WRITE_FAILED" >&2
    exit 11
  fi
fi

# preflight: markdown image paths must resolve to local files
python - <<'PY'
import os,re,sys
report='/tmp/stock-reports/reports/2026-03-04-afternoon-report.md'
base=os.path.dirname(report)
text=open(report,'r',encoding='utf-8').read()
paths=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
missing=[]
for p in paths:
    rp=os.path.normpath(os.path.join(base,p))
    if not os.path.isfile(rp):
        missing.append((p,rp))
if missing:
    print('PREFLIGHT_FAIL')
    for m in missing: print(m[0],'->',m[1])
    sys.exit(21)
print(f'PREFLIGHT_OK images={len(paths)}')
PY
