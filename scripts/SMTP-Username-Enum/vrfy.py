#!/usr/bin/python3
import socket
import sys
if len(sys.argv) != 3:
 print("Usage: vrfy.py <target IP> <username list>")
 sys.exit(0)
# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the Server
connect = s.connect((sys.argv[1],25))
# Receive the banner
banner = s.recv(1024).decode("utf-8")
print("Server Banner: " + banner)
# Open file
f = open(sys.argv[2],'r')
# VRFY a user
for user in f.readlines():
  s.send(('VRFY ' + user).encode('utf-8'))
  result = s.recv(1024).decode("utf-8")
  if "rejected" not in result:
    print("User Found: " + user)
# Close the socket
s.close()
