import time
import pandas as pd
from SmartApi import SmartConnect
import datetime
import json
import pyotp
import numpy as np

# ✅ Angel One API Credentials
API_KEY = "DfqxqRnd"
CLIENT_ID = "A507943"
MPIN = "1181"
TOTP_SECRET = "HBZNZU7YCG35O4JHTE622JC64Q"

# ✅ Initialize Angel One API
obj = SmartConnect(api_key=API_KEY)

# ✅ Generate TOTP & Login
totp = pyotp.TOTP(TOTP_SECRET).now()

login_response = obj.generateSession(
    clientCode=CLIENT_ID,
    password=MPIN,
    totp=totp
)

if not login_response.get("status"):
    print(f"❌ Login failed: {login_response.get('message', 'Unknown error')}")
    exit()

print("✅ Angel One Login Successful!")

# ✅ Define Time Frames to Fetch
time_frames = [
    "ONE_MINUTE", "TWO_MINUTE", "THREE_MINUTE",
    "FIVE_MINUTE", "TEN_MINUTE", "FIFTEEN_MINUTE",
    "THIRTY_MINUTE", "ONE_HOUR"
]

# ✅ Function to Fetch Intraday Historical Data
def fetch_intraday_data(stock_name, stock_token, interval, days=90):
    print(f"📊 Fetching {interval} data for {stock_name}...")

    # ✅ Get the current date & calculate past date
    to_date = datetime.datetime.today()
    from_date = to_date - datetime.timedelta(days=days)

    # ✅ Format dates for Angel One API (FIXED FORMAT)
    from_date_str = from_date.strftime("%Y-%m-%d %H:%M")  # No seconds
    to_date_str = to_date.strftime("%Y-%m-%d %H:%M")      # No seconds

    params = {
        "exchange": "NSE",
        "symboltoken": stock_token,
        "interval": interval,
        "fromdate": from_date_str,
        "todate": to_date_str,
    }

    try:
        response = obj.getCandleData(params)
        if response and response["status"]:
            data = response["data"]
            df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
            df["datetime"] = pd.to_datetime(df["datetime"])

            # ✅ Calculate Additional Indicators
            df['Price Movement'] = df['high'] - df['low']
            df['ATR'] = df['Price Movement'].rolling(14).mean()
            df['VWAP'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()

            # ✅ RSI Calculation
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            # ✅ Moving Averages
            df['SMA_9'] = df['close'].rolling(window=9).mean()
            df['SMA_21'] = df['close'].rolling(window=21).mean()

            # ✅ Save as CSV
            file_path = f"trade-tracker/data/{stock_name}_{interval}.csv"
            df.to_csv(file_path, index=False)
            print(f"✅ Data saved: {file_path}")
        else:
            print(f"❌ API Fetch Error for {stock_name} [{interval}]: {response.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"⚠️ Error fetching data for {stock_name} [{interval}]: {str(e)}")

# ✅ Fetch Data for Tata Power in Different Time Frames
tata_power = {"name": "TATA_POWER", "token": "3456"}  # Replace with correct token if needed

for interval in time_frames:
    fetch_intraday_data(tata_power["name"], tata_power["token"], interval=interval, days=90)
    time.sleep(2)  # Prevent hitting API rate limits

# ✅ Logout
obj.terminateSession(clientCode=CLIENT_ID)
print("✅ Logged out of Angel One")
