import os
import sys

#usage: python3 subdomain.py https example.com
#usage: python3 subdomain.py http outdated.htb "-fc 301"

args = sys.argv

protocol = args[1]
domain = args[2]

if len(args) > 3:
    flags = " " + sys.argv[3]
else:
    flags = ""

cmd = f'ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.{domain}" -fc 400,403 -fl 8 -u {protocol}://{domain}{flags}'

print("Running: " + cmd)
os.system(cmd)
