import requests

API_KEY = "nyklK2ko"
CLIENT_CODE = "A507943"
PASSWORD = "11811Xx@@@"
TOT_PWD = "HBZNZU7YCG35O4JHTE622JC64Q"

url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
headers = {
    "Content-Type": "application/json",
    "X-ClientLocalIP": "127.0.0.1",
    "X-ClientPublicIP": "127.0.0.1",
    "X-MACAddress": "00:1A:2B:3C:4D:5E",
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "X-ClientID": CLIENT_CODE,
    "X-APIKey": API_KEY,
}
data = {
    "clientcode": CLIENT_CODE,
    "password": PASSWORD,
    "totp": TOT_PWD
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
