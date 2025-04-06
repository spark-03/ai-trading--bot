from smartapi import SmartConnect
import pyotp

# 🔹 Replace with your credentials
API_KEY = "RLETHV6X"
CLIENT_ID = "A507943"
MPIN = "1181"  # ⚠️ Replace with your actual MPIN
TOTP_SECRET = "HBZNZU7YCG35O4JHTE622JC64Q"

# 🔹 Initialize SmartAPI connection
obj = SmartConnect(api_key=API_KEY)

# 🔹 Generate TOTP for login
totp = pyotp.TOTP(TOTP_SECRET).now()

# 🔹 Authenticate using MPIN
login_response = obj.generateSession(
    clientCode=CLIENT_ID,
    password=MPIN,  # MPIN instead of password
    totp=totp,
    isMpin=True  # ⚠️ Important for MPIN login
)

# 🔹 Check login status
if login_response.get('status'):
    print("✅ Login successful!")
    feed_token = obj.getfeedToken()
else:
    print(f"❌ Login failed: {login_response.get('message', 'Unknown error')}")
    exit()

# 🔹 Fetch Market Data (Reliance Example)
params = {
    "exchange": "NSE",
    "tradingsymbol": "RELIANCE",
    "symboltoken": "2885"
}

market_data = obj.getQuote(params)
print("📊 Market Data:", market_data)
