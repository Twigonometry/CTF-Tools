import requests
import netifaces as ni

ni.ifaddresses('tun0')
ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']
print(ip)

