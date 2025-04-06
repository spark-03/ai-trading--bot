import time
import requests
import pandas as pd
import numpy as np
from SmartApi import SmartConnect
import pyotp
import json
from datetime import datetime

# 🔹 Function to Log Trades
def log_trade(symbol, buy_price, sell_price):
    trade = {
        "id": str(datetime.now().timestamp()),
        "symbol": symbol,
        "buyPrice": buy_price,
        "sellPrice": sell_price,
        "profitLoss": round(sell_price - buy_price, 2),
        "time": datetime.now().isoformat()
    }

    url = "http://localhost:5000/trades"

    response = requests.post(url, data=json.dumps(trade), headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        print("✅ Trade logged successfully:", trade)
    else:
        print("❌ Failed to log trade:", response.text)

# ✅ Angel One API Credentials
API_KEY = "DfqxqRnd"
CLIENT_ID = "A507943"
MPIN = "1181"  # ✅ MPIN used instead of password
TOTP_SECRET = "HBZNZU7YCG35O4JHTE622JC64Q"

# ✅ Initialize Smart API
obj = SmartConnect(api_key=API_KEY)
totp = pyotp.TOTP(TOTP_SECRET).now()

# ✅ Authenticate using MPIN
login_response = obj.generateSession(
    clientCode=CLIENT_ID,
    password=MPIN,
    totp=totp
)

if not login_response.get("status"):
    print(f"❌ Login failed: {login_response.get('message', 'Unknown error')}")
    exit()

feed_token = obj.getfeedToken()
print("✅ Login Successful!")

# ✅ Market Data Parameters
EXCHANGE = "NSE"
SYMBOL = "RELIANCE"
SYMBOL_TOKEN = "2885"

# Function to fetch latest market data (LIVE)
def fetch_market_data():
    try:
        response = obj.ltpData(EXCHANGE, SYMBOL, SYMBOL_TOKEN)
        if response.get("status"):
            return response["data"]["ltp"]
    except Exception as e:
        print(f"⚠️ Error fetching market data: {e}")
    return None

# Function to calculate VWAP, RSI, and EMA crossover
def calculate_indicators(df):
    df["VWAP"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()
    df["EMA_9"] = df["close"].ewm(span=9, adjust=False).mean()
    df["EMA_21"] = df["close"].ewm(span=21, adjust=False).mean()

    delta = df["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

# Function to check buy/sell signals
def check_trade_signals(df):
    latest = df.iloc[-1]

    if latest["close"] > latest["VWAP"] and latest["RSI"] < 30 and latest["EMA_9"] > latest["EMA_21"]:
        return "BUY"
    elif latest["close"] < latest["VWAP"] and latest["RSI"] > 70 and latest["EMA_9"] < latest["EMA_21"]:
        return "SELL"
    return "HOLD"

# ✅ Running the Trading Bot
market_data = []
paper_trades = []

while True:
    ltp = fetch_market_data()
    if ltp:
        print(f"📈 Latest Price: {ltp}")
        market_data.append({"close": ltp, "volume": 1000})  # Assuming volume data
        if len(market_data) > 50:
            df = pd.DataFrame(market_data)
            df = calculate_indicators(df)
            signal = check_trade_signals(df)

            if signal == "BUY":
                buy_price = ltp
                paper_trades.append({"symbol": SYMBOL, "buy_price": buy_price, "time": time.time()})
                print(f"🚀 Placed Paper Trade: BUY at {buy_price}")

            elif signal == "SELL" and len(paper_trades) > 0:
                last_trade = paper_trades.pop(0)  # Sell the earliest trade
                sell_price = ltp
                profit_loss = sell_price - last_trade["buy_price"]

                log_trade(SYMBOL, last_trade["buy_price"], sell_price)
                print(f"✅ Trade closed: Sold at {sell_price}, P/L: {profit_loss}")

    time.sleep(5)  # Fetch data every 5 seconds
