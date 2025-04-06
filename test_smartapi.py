from SmartApi import SmartConnect

# Replace with your Angel One credentials
API_KEY = "OdWEjLOq "
CLIENT_ID = "A507943"  # This is your Angel One User ID
PASSWORD = "1181"
TOTP = "HBZNZU7YCG35O4JHTE622JC64Q"  # Only required if 2FA is enabled

try:
    # Initialize connection
    obj = SmartConnect(api_key=API_KEY)
    
    # Generate session (with TOTP if required)
    data = obj.generateSession(
        clientID=CLIENT_ID,
        password=PASSWORD,
        # totp=TOTP  # Uncomment if you have 2FA enabled
    )
    
    # Check if authentication was successful
    if data['status'] == False:
        print(f"Authentication failed: {data['message']}")
        exit()
    
    print("Authentication successful!")
    print("Auth Token:", data['data']['jwtToken'])
    print("Refresh Token:", data['data']['refreshToken'])
    
    # Fetch profile data
    profile = obj.getProfile()
    print("\nProfile Data:")
    print(profile)

except SmartExceptions.SmartAPIException as e:
    print(f"SmartAPI Exception: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")