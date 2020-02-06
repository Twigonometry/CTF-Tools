import hashlib
import json

ALGORITHM_NAMES = {"1": "MD5", "2": "SHA-1"}

def load_wordlist(file_path):
    """load a wordlist from file"""

    print("Attempting to load word list from /wordlists/" + file_path + "\n")
    wordlist = list()
    f = open("wordlists/" + file_path, "r")
    if(f.mode == 'r'):
        lines = f.readlines()
        for line in lines:
            wordlist.append(line.strip())

    return wordlist

def brute_force(hashedpass, wordlist, alg_name):
    """brute force a wordlist using a given algorithm, outputting the password"""

    found = False

    print("Running brute force attack using " + alg_name)

    for word in wordlist:
        if alg_name == "MD5":
            hash = hashlib.md5(word.encode('utf-8')).hexdigest()
        if hash == hashedpass:
            found = True
            print("Match found:")
            print("Password: " + word)
            print("Hash: " + hash)
            print()
            break

    if not found:
        print("No match found")

def brute_force_dict(hashedpass, file_path, alg_name):
    """brute force attack using precomputed hash dictionary"""

    print("Running dictionary attack using " + alg_name)

    split_path = file_path.split(".")
    new_path = split_path[0] + "_" + alg_name + "." + split_path[1]

    hash_dict = load_dictionary(new_path)
    found = False
    
    for key in hash_dict:
        if hashedpass == hash_dict[key]:
            print("Match found:")
            print("Password: " + key)
            print("Hash: " + hashedpass)
            print()
            found = True
            break
    
    if not found:
        print("No match found")

def generate_dictionary(file_path, alg_name):
    """generate a dictionary by hashing all passwords in a wordlist
    and save this dictionary to file"""

    wordlist = load_wordlist(file_path)
    hash_dict = {}

    for word in wordlist:
        if alg_name == "MD5":
            hash = hashlib.md5(word.encode('utf-8')).hexdigest()
        elif alg_name == "SHA-1":
            hash = hashlib.sha1(word.encode('utf-8')).hexdigest()
        hash_dict[word] = hash

    split_path = file_path.split(".")
    new_path = "wordlists/" + split_path[0] + "_dict_" + alg_name + "." + split_path[1]
    print("New dictionary created at: " + new_path)
    
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

def crack_list(hash_list, file_path):
    """crack a list of hashes"""
    
    #select method
    method = input("Select attack method:\n1. Brute Force \n2. Brute Force Dictionary\n")

    #select hashing algorithm
    alg_choice = input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n")
    alg_name = ALGORITHM_NAMES[alg_choice]

    #iterate over list
    if method == "1":
        wordlist = load_wordlist(file_path)
        for hash in hash_list:
            brute_force(hash, wordlist, alg_name)
    elif method == "2":
        split_path = file_path.split(".")
        new_path = "wordlists/" + split_path[0] + "_dict." + split_path[1]
        
        for hash in hash_list:
            brute_force_dict(hash, new_path, alg_name)

def main():
    generate_dictionary("rockyou-25.txt", "SHA-1")

if __name__ == "__main__":
    main()