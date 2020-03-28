# Hack the Box

Various scripts, exploits, and helper functions used for Hack the Box

As machines retire, I will upload the scripts used on those machines here

## Traceback

ssh.lua was used to upload my ssh public key to the sysadmin's ~/.ssh/authorized_keys file to allow privelege escalation to the sysadmin user

This was possible because of sudo priveleges for the webadmin user on /home/sysadmin/luvit, allowing you to run sudo -u sysadmin /home/sysadmin/luvit ssh.lua