import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📌 Fetch last one month's historical data
symbol = "RELIANCE.NS"  # Change this to any stock you want to analyze
data = yf.download(symbol, period="1mo", interval="1d")

# ✅ Calculate Indicators
data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()

# ✅ Generate Buy/Sell Signals
data['Signal'] = 0
data.loc[data['SMA_10'] > data['EMA_9'], 'Signal'] = 1  # Buy Signal
data.loc[data['SMA_10'] < data['EMA_9'], 'Signal'] = -1 # Sell Signal

# ✅ Calculate Strategy Performance
data['Daily_Return'] = data['Close'].pct_change()
data['Strategy_Return'] = data['Signal'].shift(1) * data['Daily_Return']

# ✅ Performance Metrics
def calculate_performance(data):
    total_profit = data['Strategy_Return'].sum() * 100  # Total return %
    win_trades = (data['Strategy_Return'] > 0).sum()
    total_trades = (data['Signal'] != 0).sum()
    win_rate = (win_trades / total_trades) * 100 if total_trades > 0 else 0
    
    cumulative_returns = (1 + data['Strategy_Return']).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min() * 100
    
    return total_profit, win_rate, max_drawdown

total_profit, win_rate, max_drawdown = calculate_performance(data)

print(f"📊 Total Profit: {total_profit:.2f}%")
print(f"✅ Win Rate: {win_rate:.2f}%")
print(f"⚠️ Max Drawdown: {max_drawdown:.2f}%")

# 📈 Plot Results
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['SMA_10'], label='SMA 10', color='red')
plt.plot(data['EMA_9'], label='EMA 9', color='green')
plt.legend()
plt.title(f'{symbol} - SMA & EMA Crossover Backtest (Last 1 Month)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
