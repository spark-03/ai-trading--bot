import pandas as pd

# ✅ Load Historical Data
file_1min = "trade-tracker/data/TATA_POWER_ONE_MINUTE.csv"
file_5min = "trade-tracker/data/TATA_POWER_FIVE_MINUTE.csv"

df_1min = pd.read_csv(file_1min)
df_5min = pd.read_csv(file_5min)

# ✅ Convert 'datetime' Column to Datetime Format
df_1min["datetime"] = pd.to_datetime(df_1min["datetime"])
df_5min["datetime"] = pd.to_datetime(df_5min["datetime"])

# ✅ Define Trading Strategy Function
def execute_trades(df, timeframe):
    print(f"\n🚀 Running Strategy on {timeframe} Data...")

    trades = []  # Store trade details

    for i in range(1, len(df)):  
        row = df.iloc[i]
        prev_row = df.iloc[i-1]

        entry_time = row["datetime"]
        entry_price = row["close"]
        target_price = entry_price * 1.005   # 0.5% target
        stop_loss = entry_price * 0.985      # 1.5% stop loss

        strategy_used = None
        exit_price = None
        exit_time = None
        profit_loss = None

        # ✅ Strategy 1: VWAP Breakout + RSI Confirmation
        if row["close"] > row["VWAP"] and row["RSI"] > 55:
            strategy_used = "VWAP + RSI"
        
        # ✅ Strategy 2: SMA 9/21 Crossover
        if prev_row["SMA_9"] < prev_row["SMA_21"] and row["SMA_9"] > row["SMA_21"]:
            strategy_used = "SMA Crossover"
        
        # ✅ Strategy 3: ATR Breakout (Volatility-Based)
        if row["close"] > prev_row["high"] + (1.5 * row["ATR"]):
            strategy_used = "ATR Breakout"

        # ✅ Execute Trade if a Strategy is Matched
        if strategy_used:
            # Simulate exit after 3 candles
            exit_index = min(i + 3, len(df) - 1)
            exit_time = df.iloc[exit_index]["datetime"]
            exit_price = df.iloc[exit_index]["close"]
            profit_loss = round(exit_price - entry_price, 2)

            trades.append([entry_time, entry_price, exit_time, exit_price, profit_loss, strategy_used, timeframe])

    # ✅ Print Trade Signals
    if trades:
        print("📊 Trade Signals Found:")
        for trade in trades:
            print(f"📌 {trade[0]} | Entry: {trade[1]} | Exit: {trade[3]} | P/L: {trade[4]} | Strategy: {trade[5]} | TF: {trade[6]}")
    else:
        print("❌ No Trade Signals Found!")

    return trades

# ✅ Run Strategy on Both Timeframes
trades_1min = execute_trades(df_1min, "1-Min")
trades_5min = execute_trades(df_5min, "5-Min")

# ✅ Save Results to Excel
df_results = pd.DataFrame(trades_1min + trades_5min, columns=["Entry Time", "Entry Price", "Exit Time", "Exit Price", "Profit/Loss", "Strategy", "Timeframe"])
df_results.to_excel("trade_results.xlsx", index=False)

print("\n✅ Trades saved to 'trade_results.xlsx' for better analysis! 📂")
