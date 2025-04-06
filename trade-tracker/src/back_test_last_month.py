import pandas as pd
import ta

# ✅ Load Historical Data
file_path = "trade-tracker/data/TATA_POWER_ONE_MINUTE.csv"
df = pd.read_csv(file_path)

# ✅ Convert 'datetime' Column to Datetime Format
df["datetime"] = pd.to_datetime(df["datetime"])

# ✅ Define Brokerage & Charges
BROKERAGE_PERCENTAGE = 0.02 / 100  # 0.02% per trade
OTHER_FEES = 0.01 / 100  # Misc fees
FIXED_BROKERAGE = 40  # ₹40 per trade
TRADE_CAPITAL = 50000  # ₹50,000 per trade

# ✅ Compute Indicators using `ta` Library
df['VWAP'] = (df['high'] + df['low'] + df['close']) / 3  # Approximate VWAP
df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
df['EMA_9'] = ta.trend.EMAIndicator(df['close'], window=9).ema_indicator()
df['EMA_21'] = ta.trend.EMAIndicator(df['close'], window=21).ema_indicator()
macd = ta.trend.MACD(df['close'])
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()
df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
df['Volume_MA_20'] = df['volume'].rolling(window=20).mean()

def calculate_stop_loss_target(entry_price, atr):
    return entry_price - (atr * 2.5), entry_price + (atr * 3)

# ✅ Execute Trades
trades = []
in_position = False
position_type = None  # "long" or "short"
entry_price = 0
entry_time = None
shares = 0
target_price = 0
stop_loss = 0
MIN_HOLD_TIME = pd.Timedelta(minutes=10)  # Prevent exiting too soon

for i in range(1, len(df)):
    row = df.iloc[i]
    prev_row = df.iloc[i - 1]
    high_volume = row["volume"] > row["Volume_MA_20"]
    atr = row['ATR']

    if not in_position and high_volume and atr > 0:
        stop_loss, target_price = calculate_stop_loss_target(row['close'], atr)
        
        if row['close'] > row['VWAP'] and row['RSI'] > 55 and row['EMA_9'] > row['EMA_21'] and row['MACD'] > row['MACD_Signal']:
            in_position = True
            position_type = "long"
            entry_price = row['close']
            entry_time = row['datetime']
            shares = TRADE_CAPITAL // entry_price

        elif row['close'] < row['VWAP'] and row['RSI'] < 45 and row['EMA_9'] < row['EMA_21'] and row['MACD'] < row['MACD_Signal']:
            in_position = True
            position_type = "short"
            entry_price = row['close']
            entry_time = row['datetime']
            shares = TRADE_CAPITAL // entry_price

    elif in_position:
        time_in_trade = row['datetime'] - entry_time
        macd_exit_signal = (row['MACD'] < row['MACD_Signal'] and position_type == "long") or \
                           (row['MACD'] > row['MACD_Signal'] and position_type == "short")
        trailing_stop = entry_price + (atr * 1.5) if position_type == "long" else entry_price - (atr * 1.5)

        if time_in_trade >= MIN_HOLD_TIME and ((position_type == "long" and (row['close'] >= target_price or row['close'] <= stop_loss or row['close'] < trailing_stop)) or \
           (position_type == "short" and (row['close'] <= target_price or row['close'] >= stop_loss or row['close'] > trailing_stop))):
            exit_price = row['close']
            exit_time = row['datetime']
            gross_profit_loss = (exit_price - entry_price) * shares if position_type == "long" else (entry_price - exit_price) * shares
            trade_value = (entry_price + exit_price) * shares
            brokerage_fees = trade_value * (BROKERAGE_PERCENTAGE + OTHER_FEES) + FIXED_BROKERAGE
            net_profit_loss = gross_profit_loss - brokerage_fees
            trades.append([entry_time, entry_price, exit_time, exit_price, shares, gross_profit_loss, net_profit_loss, position_type])
            in_position = False

# ✅ Convert Trades to DataFrame
df_trades = pd.DataFrame(trades, columns=["Entry Time", "Entry Price", "Exit Time", "Exit Price", "Shares", "Gross P/L", "Net P/L", "Trade Type"])
df_trades["Entry Time"] = df_trades["Entry Time"].dt.tz_localize(None)
df_trades["Exit Time"] = df_trades["Exit Time"].dt.tz_localize(None)
df_trades.to_excel("trade_results.xlsx", index=False)
print("\n✅ Trades saved to 'trade_results.xlsx' successfully!")
import pandas as pd
import numpy as np
from ta import add_all_ta_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. Data Loading & Feature Engineering
file_path = "trade-tracker/data/TATA_POWER_ONE_MINUTE.csv"
df = pd.read_csv(file_path)
df["datetime"] = pd.to_datetime(df["datetime"])

# Use ta library to add many indicators at once (you can choose specific ones if preferred)
df = add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume", fillna=True)

# 2. Labeling the Data
# For simplicity, label a trade as profitable if the 5-minute forward return is >0.5%
df["future_return"] = df["close"].shift(-5) / df["close"] - 1
df["profit_label"] = np.where(df["future_return"] > 0.005, 1, 0)

# Drop rows with NaNs created by shifting
df.dropna(inplace=True)

# 3. Feature Selection
# For a start, select a subset of features. You can experiment with more:
features = [
    "volume_adi", "volume_obv", "momentum_rsi", "trend_macd", "trend_macd_signal",
    "volatility_atr", "trend_ema_fast", "trend_ema_slow"
]
X = df[features]
y = df["profit_label"]

# 4. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 5. Model Training
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 6. Predictions & Evaluation
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# 7. (Optional) Save Model and Features for Live Trading
import joblib
joblib.dump(clf, "trade_model.pkl")
joblib.dump(features, "model_features.pkl")

print("Model training complete and saved!")
