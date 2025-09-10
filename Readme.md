# SMC/ICT Full Candle EA – MT4 / MT5

## Description
The **SMC/ICT Full Candle EA** is a professional multi-symbol Expert Advisor designed for traders following **Smart Money Concepts (SMC) and Inner Circle Trader (ICT) strategies**. It automates the detection of market structures, zones, and liquidity levels to provide accurate trade signals and execution.

The EA is optimized for **BTC/USD weekend trading**, while also supporting major assets like XAU/USD, GBP/JPY, EUR/USD, and US30 during standard trading hours.

## Features

### ICT / SMC Trade Logic
- Bullish/Bearish Order Blocks (OB)
- Fair Value Gaps (FVG)
- Breaker Blocks
- Liquidity Sweeps
- Multi-Timeframe Analysis:
  - Trend Detection (H1)
  - Entry Zone Detection (M15)
  - Microstructure Confirmation (M5)

### Trade Execution
- Zone-based Stop Loss and Take Profit
- Dynamic lot sizing based on account risk
- Configurable maximum trades per symbol
- Session-aware trading:
  - BTC/USD trades 24/7
  - Other symbols trade only during specified hours

### Alerts & Notifications
- Telegram push notifications with full trade and zone details
- Real-time MT4/MT5 log alerts

### Full Logging / Excel Integration
- Excel-ready CSV log files
- Logged data per trade:
  - Timestamp, Symbol, Direction (BUY/SELL)
  - OB, FVG, Breaker, Liquidity Sweep Levels
  - SL / TP
  - Lot size
  - Trade Result

### Multi-Symbol & Multi-Timeframe Support
- Trade multiple symbols simultaneously
- Configurable timeframes for trend, entry, and microstructure confirmation

### User Configurable Parameters
- Symbols and timeframes
- Risk % per trade
- Max trades per symbol
- Session hours for non-BTC symbols
- Telegram Bot Token and Chat ID
- Enable/Disable Logging and Alerts

### Plug-and-Play
- MT4 and MT5 versions included
- Attach EA to any chart (symbol-agnostic)
- Fully automated with optional Telegram monitoring

## Benefits
- Fully ICT/SMC compliant with multi-timeframe precision
- Supports weekend BTC/USD trading
- Ensures risk management through zone-based SL/TP and dynamic lot sizing
- Real-time monitoring via Telegram and logs
- Offline performance analysis with Excel-ready CSV logs
