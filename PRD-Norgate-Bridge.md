# PRD: Norgate Data Bridge Server (Project "SwingAlpha-Bridge")

## 1. Overview
A lightweight Python-based API server running on Windows to bridge high-quality market data from **Norgate Data** to the **OpenClaw AI Agent** (Linux). This enables the agent to perform advanced momentum screening (Kullamägi style) without having direct access to the Norgate Windows-only local database.

## 2. Target Audience
- **Primary**: The OpenClaw AI Agent (`Sammy AI`).
- **User**: Wei Liu (for manual oversight and local execution).

## 3. Functional Requirements

### 3.1 Market Data Access (Norgate Integration)
- Connect to the local Norgate Data installation via the `norgatedata` Python library.
- Access major US equity exchanges (NYSE, NASDAQ, AMEX).
- Retrieve historical OHLCV (Open, High, Low, Close, Volume) data with adjustments for dividends and splits.

### 3.2 Scanning Engine (Kullamägi Logic)
Implement the first pass of the `swing-alpha` skill logic:
- **Momentum Filter**: Tickers with >90% gain in the last 40-60 trading days.
- **Volatility Filter**: Average Daily Range (ADR % over 20 days) > 4%.
- **Consolidation Filter**: Identifying tickers within 10% of 52-week highs with tight price action.

### 3.3 API Endpoints
The server must expose the following RESTful endpoints (using FastAPI):
- `GET /status`: Health check and Norgate database status.
- `GET /scan`: Run the market scan with customizable filters.
    - **Parameters**:
        - `min_momentum_60` (float, default: 1.3): Minimum gain over last 60 trading days (e.g., 1.3 = 30% gain).
        - `min_momentum_30` (float, default: 1.2): Minimum gain over last 30 trading days.
        - `min_adr` (float, default: 4.0): Minimum 20-day Average Daily Range percentage.
        - `max_dist_ema10` (float, default: 3.0): Max % distance from the 10-day EMA.
        - `min_volume` (int, default: 500000): Minimum 20-day average daily volume.
        - `max_pullback` (float, default: 20.0): Maximum % pullback from recent high.
- `GET /data/{ticker}`: Return raw historical data for a specific ticker (JSON format).
- `GET /chart/{ticker}`: Generate and return a PNG candlestick chart with 10/20 EMA overlays.

## 4. Technical Specifications
- **Operating System**: Windows 10/11.
- **Language**: Python 3.9+.
- **Framework**: FastAPI + Uvicorn.
- **Libraries**:
    - `norgatedata`: For database access.
    - `pandas`: For data manipulation.
    - `matplotlib` or `plotly`: For chart generation.
    - `ta-lib` (optional): For technical indicator calculation.

## 5. Security & Connectivity
- **Local Access**: Accessible via `localhost:8000` or local network IP.
- **Remote Access (Optional)**: Via Tailscale or secure tunnel if the Agent is off-site.
- **Authentication**: Simple API key header required for all requests.

## 6. Deployment Workflow
1. Install Norgate Data Windows application and Python library.
2. Run `pip install fastapi uvicorn pandas norgatedata matplotlib`.
3. Execute `python main.py` to start the bridge.
4. Agent sends requests to the bridge to fetch scan results.

---
*Created by Sammy AI for Wei Liu - 2026-02-22*
