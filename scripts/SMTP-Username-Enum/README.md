# SMTP Username Enumeration

`vrfy.py` checks an SMTP server for valid usernames via the `VRFY` command.

## Usage

First make it executable:

```bash
$ chmod +x vrfy.py
```

Then execute it, passing a target IP address/hostname and a list of usernames:

```bash
$ ./vrfy.py [IP] [WORDLIST]
```

e.g.

```bash
$ ./vrfy.py 10.0.0.1 /usr/share/seclists/Usernames/top-usernames-shortlist.txt
```
