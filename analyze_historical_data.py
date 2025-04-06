import pandas as pd
import matplotlib.pyplot as plt

# Load historical data
file_path = "historical_data.csv"  # Ensure this file exists in the same directory
data = pd.read_csv(file_path)

# Convert 'datetime' to datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Sort data by datetime
data = data.sort_values(by='datetime')

# Calculate indicators
data['EMA_9'] = data['close'].ewm(span=9, adjust=False).mean()  # Exponential Moving Average (9)
data['SMA_10'] = data['close'].rolling(window=10, min_periods=1).mean()
  # Allow calculation for shorter data

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data['datetime'], data['close'], label='Close Price', color='blue')
plt.plot(data['datetime'], data['EMA_9'], label='EMA 9', color='green')

# Only plot SMA if enough data points are available
if len(data) >= 10:
    plt.plot(data['datetime'], data['SMA_10'], label='SMA 10', color='red')

# Formatting the plot
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Stock Price with Indicators")
plt.legend()
plt.xticks(rotation=45)
plt.grid()

# Show the plot
plt.show()
