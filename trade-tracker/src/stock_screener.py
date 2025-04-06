import yfinance as yf
import pandas as pd

# ✅ List of NIFTY 100 Stocks (Replace with dynamic fetching later)
nifty_100_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "MARUTI.NS", "HINDUNILVR.NS", "BAJFINANCE.NS"]

# ✅ Define Selection Criteria
min_pre_market_change = 1.0  # % change in pre-market (at least ±1%)
min_avg_volume = 2_000_000   # Minimum 2M shares traded (liquidity)
min_atr_percent = 0.5        # ATR should be at least 0.5% of the stock price

# ✅ Data Storage
selected_stocks = []

# ✅ Fetch Pre-Market & Historical Data
for stock in nifty_100_stocks:
    try:
        print(f"🔍 Checking {stock} for tomorrow's trades...")

        # 🔹 Fetch last 5 days of data
        data = yf.download(stock, period="5d", interval="1d")

        # 🔹 Skip if no data available
        if data.empty or len(data) < 2:
            print(f"⚠️ Not enough data for {stock}, skipping...")
            continue

        # 🔹 Calculate ATR (Volatility)
        high_low = data["High"] - data["Low"]
        atr = high_low.rolling(window=5).mean()

        if atr.empty or data["Close"].empty:
            print(f"⚠️ ATR Calculation Error for {stock}, skipping...")
            continue

        avg_atr_percent = (atr.iloc[-1] / data["Close"].iloc[-1]) * 100 if len(atr.dropna()) > 0 else 0

        # 🔹 Pre-Market % Change (Using Last 2 Days Close)
        pre_market_change = ((data["Close"].iloc[-1] - data["Close"].iloc[-2]) / data["Close"].iloc[-2]) * 100

        # 🔹 Liquidity (Average Volume of last 5 days)
        avg_volume = data["Volume"].mean()

        # 🔹 Apply Filtering Criteria
        if abs(pre_market_change) >= min_pre_market_change and avg_volume > min_avg_volume and avg_atr_percent > min_atr_percent:
            selected_stocks.append({
                "Stock": stock,
                "Pre-Market % Change": round(pre_market_change, 2),
                "ATR %": round(avg_atr_percent, 2),
                "Avg Volume": int(avg_volume)
            })

    except Exception as e:
        print(f"⚠️ Error with {stock}: {e}")

# ✅ Display Best Stocks for Scalping Tomorrow
print("\n📊 **Best Stocks for Scalping Tomorrow:**")
if selected_stocks:
    df = pd.DataFrame(selected_stocks)
    print(df.to_string(index=False))
else:
    print("❌ No stocks met the criteria. Try adjusting thresholds.")
