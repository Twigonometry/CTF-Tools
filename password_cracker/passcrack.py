import hashlib
import json

def load_wordlist(filename):
    """load a wordlist from file"""

    print("Attempting to load word list from /wordlists/" + filename)
    wordlist = list()
    f = open("wordlists/" + filename, "r")
    if(f.mode == 'r'):
        lines = f.readlines()
        for line in lines:
            wordlist.append(line.strip())

    return wordlist

def brute_force(hashedpass, wordlist):
    """brute force a wordlist using a given algorithm, outputting the password"""

    choice = input("Select hashing algorithm:\n1. MD5")
    if choice=="1":
        print("Running brute force attack using MD5")
        for word in wordlist:
            hash = hashlib.md5(word.encode('utf-8')).hexdigest()
            if hash == hashedpass:
                print("password: " + word)
                print(hash)
                break

def brute_force_dict(hashedpass, file_path):
    """brute force attack using precomputed hash dictionary"""

    choice = input("Select hashing algorithm:\n1. MD5")
    if choice=="1":
        print("Running dictionary attack using MD5")
        hash_dict = load_dictionary(file_path)
        found = False
        
        for key in hash_dict:
            if hashedpass == hash_dict[key]:
                print("Match found:")
                print("Password: " + key)
                print("Hash: " + hashedpass)
                found = True
                break
        
        if not found:
            print("No match found")

def generate_dictionary(wordlist_address):
    """generate a dictionary by hashing all passwords in a wordlist
    and save this dictionary to file"""

    wordlist = load_wordlist(wordlist_address)
    hash_dict = {}
    for word in wordlist:
        hash = hashlib.md5(word.encode('utf-8')).hexdigest()
        hash_dict[word] = hash

    split_path = wordlist_address.split(".")
    new_path = "wordlists/" + split_path[0] + "_dict." + split_path[1]
    print(new_path)
    
    dict_file = open(new_path, "w")
    dict_file.write(json.dumps(hash_dict))
    dict_file.close()

def load_dictionary(file_path):
    """load a dictionary from a text file"""

    hash_dict = {}

    f = open(file_path)
    raw = f.read()
    hash_dict = json.loads(raw)

    return hash_dict

def main():
    brute_force_dict("5f4dcc3b5aa765d61d8327deb882cf99", "wordlists/rockyou-25_dict.txt")

if __name__ == "__main__":
    main()