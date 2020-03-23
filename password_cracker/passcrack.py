import hashlib
import json
import binascii
import bcrypt

ALGORITHM_NAMES = {"1": "MD5", "2": "SHA-1", "3": "SHA-256", "4": "SHA-512", "5": "NTLM", "6": "BCRYPT", "7": "CASCADE"}

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

    print(hashedpass)

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
            rounds, salt = parse_bcrypt(hashedpass)
            hash = bcrypt.hashpw(word.encode('utf-8'), salt.encode('utf-8')).decode()
            print(hash)
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
    method = input("Select attack method:\n1. Brute Force\n2. Brute Force Dictionary\n")

    #iterate over list
    if method == "1":
        #select hashing algorithm
        alg_choice = input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n3. SHA-256\n4. SHA-512\n5. NTLM\n6. BCRYPT\n7. Try above methods in order of complexity\n")
        alg_name = ALGORITHM_NAMES[alg_choice]
        
        wordlist = load_wordlist(file_path)
        if alg_name == "CASCADE":
            found = False
            
            #cascade through algorithms, stopping based on their boolean 'found' value
            for hash in hash_list:
                for alg_no in ALGORITHM_NAMES:
                    found = brute_force(hash, wordlist, ALGORITHM_NAMES[alg_no])
                    if found:
                        break

        else:
            for hash in hash_list:
                brute_force(hash, wordlist, alg_name)
    elif method == "2":
        #select hashing algorithm
        alg_choice = input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n3. SHA-256\n4. SHA-512\n5. NTLM\n6. Try above methods in order of complexity\n")
        if alg_choice == 6:
            alg_choice = 7
        alg_name = ALGORITHM_NAMES[alg_choice]

        split_path = file_path.split(".")
        new_path = "wordlists/" + split_path[0] + "_dict." + split_path[1]

        if alg_name == "CASCADE":
            found = False
            
            #cascade through algorithms, stopping based on their boolean 'found' value
            for hash in hash_list:
                for alg_no in ALGORITHM_NAMES:
                    found = brute_force_dict(hash, new_path, ALGORITHM_NAMES[alg_no])
                    if found:
                        break
        else:
            for hash in hash_list:
                brute_force_dict(hash, new_path, alg_name)

def parse_bcrypt(hash):
    """given a bcrypt hash, parse number of rounds and salt"""
    rounds = int(hash[4:6])
    #salt = hash[7:29]
    salt = hash[0:29]

    return rounds, salt

def main():
    # rounds, salt = parse_bcrypt("$2a$12$EQBIh4LldRg/hseIeCwwyO8be5iwf6YtkLpChvSGChJETJT66SwI6")

    # print(rounds)
    # print(salt)

    print("Welcome to the Password Cracker")
    main_choice = input("1. Crack hashes\n2. Generate a dictionary\n")

    if main_choice == "1":
        """crack a list of hashes"""

        hash_list = input("Enter list of hashes, separated by commas\n").replace(" ","").split(",")

        file_path = input("Enter name of wordlist to be used (should be saved in /wordlists)\n")

        crack_list(hash_list, file_path)
    elif main_choice == "2":
        """generate a dictionary of hashes"""

        alg_choice = input("Select hashing algorithm:\n1. MD5\n2. SHA-1\n3. SHA-256\n4. SHA-512\n5. NTLM\n")
        alg_name = ALGORITHM_NAMES[alg_choice]

        file_path = input("Enter name of wordlist to be used (should be saved in /wordlists)\n")

        generate_dictionary(file_path, alg_name)

if __name__ == "__main__":
    main()