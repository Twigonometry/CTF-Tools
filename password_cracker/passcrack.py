import hashlib
import json
import binascii
import bcrypt

ALGORITHM_NAMES = ["MD5","SHA-1","SHA-256","SHA-512", "NTLM","BCRYPT","CASCADE"]

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
        elif alg_name == "SHA-1":
            hash = hashlib.sha1(word.encode('utf-8')).hexdigest()
        elif alg_name == "SHA-256":
            hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
        elif alg_name == "SHA-512":
            hash = hashlib.sha512(word.encode('utf-8')).hexdigest()
        elif alg_name == "NTLM":
            hash = binascii.hexlify(hashlib.new('md4', word.encode('utf-16le')).digest()).decode()
        elif alg_name == "BCRYPT":
            salt = hashedpass[0:29]
            hash = bcrypt.hashpw(word.encode('utf-8'), salt.encode('utf-8')).decode()
        if hash == hashedpass:
            found = True
            print("Match found:")
            print("Password: " + word)
            print("Hash: " + hash)
            print()
            break

    if not found:
        print("No match found")

    return found

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

    return found

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
        elif alg_name == "SHA-256":
            hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
        elif alg_name == "SHA-512":
            hash = hashlib.sha512(word.encode('utf-8')).hexdigest()
        elif alg_name == "NTLM":
            hash = binascii.hexlify(hashlib.new('md4', word.encode('utf-16le')).digest()).decode()
        hash_dict[word] = hash

    split_path = file_path.split(".")
    new_path = "wordlists/" + split_path[0] + "_dict_" + alg_name + "." + split_path[1]
    
    dict_file = open(new_path, "w")
    dict_file.write(json.dumps(hash_dict))
    dict_file.close()
    
    print("New dictionary created at: " + new_path)

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
    method = 0

    while method < 1 or method > 2:
        try:
            method = int(input("Select attack method:\n1. Brute Force\n2. Brute Force Dictionary\n"))
        except:
            print("Please enter an integer, 1 or 2.")

    #iterate over list
    if method == 1:
        #select hashing algorithm
        alg_choice = 0
        while alg_choice < 1 or alg_choice > 7:
            try:
                alg_choice = int(input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n3. SHA-256\n4. SHA-512\n5. NTLM\n6. BCRYPT\n7. Cascade: Try above methods in order of complexity\n"))
            except:
                print("Please enter an integer")
        alg_name = ALGORITHM_NAMES[alg_choice - 1]
        
        wordlist = load_wordlist(file_path)
        if alg_name == "CASCADE":
            
            #cascade through algorithms, stopping based on their boolean 'found' value
            for hash in hash_list:
                for i in range(0, 6):
                    if brute_force(hash, wordlist, ALGORITHM_NAMES[i]):
                        break

        else:
            for hash in hash_list:
                brute_force(hash, wordlist, alg_name)
    elif method == 2:
        #select hashing algorithm
        alg_choice = 0
        while alg_choice < 1 or alg_choice > 6:
            try:
                alg_choice = int(input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n3. SHA-256\n4. SHA-512\n5. NTLM\n6. Cascade: Try above methods in order of complexity\n"))
            except:
                print("Please enter an integer")
        if alg_choice < 6:
            alg_name = ALGORITHM_NAMES[alg_choice - 1]
        else:
            alg_name = "CASCADE"

        split_path = file_path.split(".")
        new_path = "wordlists/" + split_path[0] + "_dict." + split_path[1]

        if alg_name == "CASCADE":
            
            #cascade through algorithms, excluding bcrypt, stopping based on their boolean 'found' value
            for hash in hash_list:
                for i in range(0, 5):
                    if brute_force_dict(hash, new_path, ALGORITHM_NAMES[i]):
                        break
        else:
            for hash in hash_list:
                brute_force_dict(hash, new_path, alg_name)

def main():

    print("Welcome to the Password Cracker")
    
    main_choice = 0

    while main_choice < 1 or main_choice > 2:
        try:
            main_choice = int(input("1. Crack hashes\n2. Generate a dictionary\n"))
        except:
            print("Please enter an integer, 1 or 2.")

    if main_choice == 1:
        """crack a list of hashes"""

        hash_list = input("Enter list of hashes, separated by commas\n").replace(" ","").split(",")

        file_path = input("Enter name of wordlist to be used (should be saved in /wordlists)\n")

        crack_list(hash_list, file_path)
    elif main_choice == 2:
        """generate a dictionary of hashes"""

        alg_choice = input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n3. SHA-256\n4. SHA-512\n5. NTLM\n")
        alg_name = ALGORITHM_NAMES[alg_choice]

        file_path = input("Enter name of wordlist to be used (should be saved in /wordlists)\n")

        generate_dictionary(file_path, alg_name)

if __name__ == "__main__":
    main()