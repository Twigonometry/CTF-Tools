import os
import sys

protocol = sys.argv[1]
domain = sys.argv[2]

cmd = f'ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.{domain}" -fc 400,403 -fl 8 -u {protocol}://{domain}'

print("Running: " + cmd)
os.system(cmd)
