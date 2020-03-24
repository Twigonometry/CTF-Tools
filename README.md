# CTF-Tools
Scripts for CTFs and pentest practice

## Repeater
Provides functionality for repeating GET/POST requests, with 'payload' options similar to Burp Suite that iterate over a range of numbers.

## Password Cracker
Password cracker using precomputed hash dictionaries with various algorithms, operating over a given wordlist. This wordlist **must be saved** in the CTF-Tools/password_cracker/wordlists directory beforehand.

When typing the name of the wordlist, ensure you include the file extension! For example,

```
Enter name of wordlist to be used (should be saved in /wordlists)
rockyou-25.txt
```

When running passcrack.py, **make sure you are in the CTF-Tools/password_cracker directory**, otherwise the password cracker will not be able to find the chosen wordlist.

### Brute Force Attack

Supports MD5, SHA-1, SHA-256, SHA-512, NTLM & bcrypt hashes. Can be used with Cascade option, as detailed below, to iterate over each hashing method.

Given a wordlist and list of hashes, the brute force method will hash each word in the wordlist and compare it to the current hash. If there is a match, it will output the password and move on to the next hash in the list.

When attacking a bcrypt hash, the password cracker will automatically parse the salt from the hash. Due to the nature of bcrypt, this hashing method is slow in comparison, but it works given enough time!

### Dictionary Attack

Supports MD5, SHA-1, SHA-256, SHA-512 & NTLM hashes. Given a precomputed dictionary of hashes, the algorithm will check against the hash of each common password, eliminating the need to hash each one and speeding up your cracking.

This requires some setup; the 'Generate a dictionary' option on the main menu can be used to create a dictionary for any of the above algorithms. Generating this dictionary may take some time, but it will massively speed up future password cracking.

Given a wordlist that is stored in the CTF-Tools/password_cracker/wordlists directory, e.g. rockyou.txt, an MD5 dictionary will be created with the filename rockyou_dict_MD5. For example,

```
Welcome to the Password Cracker
1. Crack hashes
2. Generate a dictionary
2
Select hashing algorithm:
1. MD5
2. SHA-1
3. SHA-256
4. SHA-512
5. NTLM
1
Enter name of wordlist to be used (should be saved in /wordlists)
rockyou-25.txt
Attempting to load word list from /wordlists/rockyou-25.txt

New dictionary created at: wordlists/rockyou-25_dict_MD5.txt
```

bcrypt is not available as a dictionary attack, as the algorithm automatically includes a random salt (therefore, the same password could be encrypted differently twice and not easily looked up in a dictionary).

### Cascade

The Cascade option can be chosen to iterate over each hashing algorithm, in case you do not know the format of the hash you are trying to crack. Cascade does this in order of complexity of the hash, increasing the average speed.

For example, here a user may enter two hashes whose nature is unknown:

```
Enter list of hashes, separated by commas
f78f2477e949bee2d12a2c540fb6084f, c22b315c040ae6e0efee3518d830362b
```

The user could select the Cascade option with the brute force attack method (Cascade also works with a dictionary attack, assuming a dictionary has been generated for every hashing algorithm except bcrypt):

```
Select hashing algorithm:
1. MD5
2. SHA-1
3. SHA-256
4. SHA-512
5. NTLM
6. BCRYPT
7. Cascade: Try above methods in order of complexity
7
```

And the password cracker will iterate over each algorithm until it finds a match. As seen below, if it finds a match it will stop early:

```
Running brute force attack using MD5
Match found:
Password: tigger
Hash: f78f2477e949bee2d12a2c540fb6084f

Running brute force attack using MD5
No match found
Running brute force attack using SHA-1
No match found
Running brute force attack using SHA-256
No match found
Running brute force attack using SHA-512
No match found
Running brute force attack using NTLM
Match found:
Password: 123456789
Hash: c22b315c040ae6e0efee3518d830362b
```

### Wordlists

*rockyou-25.txt* contains the top 25 rockyou passwords.

*rockyou-75.txt* is the full rockyou list, in descending order of frequency, obtained from the following link
https://github.com/danielmiessler/SecLists/tree/master/Passwords/Leaked-Databases

### Mangle Map
mangle_map.txt provides a list of tuples that will be used to 'mangle' plaintext passwords and rehash them.