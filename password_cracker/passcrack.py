import hashlib
import json

def load_wordlist(filename):
    """load a wordlist from file"""

    print("Attempting to load word list from /wordlists/" + filename + "\n")
    wordlist = list()
    f = open("wordlists/" + filename, "r")
    if(f.mode == 'r'):
        lines = f.readlines()
        for line in lines:
            wordlist.append(line.strip())

    return wordlist

def brute_force(hashedpass, wordlist, choice):
    """brute force a wordlist using a given algorithm, outputting the password"""

    if choice=="1":
        print("Running brute force attack using MD5")
        found = False

        for word in wordlist:
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

def brute_force_dict(hashedpass, file_path, choice):
    """brute force attack using precomputed hash dictionary"""

    if choice=="1":
        print("Running dictionary attack using MD5")
        hash_dict = load_dictionary(file_path)
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

def crack_list(hash_list, file_path):
    #select method
    method = input("Select attack method:\n1. Brute Force \n2. Brute Force Dictionary\n")

    #select hashing algorithm
    choice = input("Select hashing algorithm:\n1. MD5\n")

    #iterate over list
    if method == "1":
        wordlist = load_wordlist(file_path)
        for hash in hash_list:
            brute_force(hash, wordlist, choice)
    elif method == "2":
        split_path = file_path.split(".")
        new_path = "wordlists/" + split_path[0] + "_dict." + split_path[1]
        
        for hash in hash_list:
            brute_force_dict(hash, new_path, choice)

def main():
    hash_list = ["e10adc3949ba59abbe56e057f20f883e", "827ccb0eea8a706c4c34a16891f84e7b", "f78f2477e949bee2d12a2c540fb6084f"]
    crack_list(hash_list, "rockyou-25.txt")

if __name__ == "__main__":
    main()