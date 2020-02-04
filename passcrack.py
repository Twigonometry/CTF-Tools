import hashlib
import json

def load_wordlist(filename):
    print("Attempting to load word list from /wordlists/" + filename)
    wordlist = list()
    f = open("wordlists/" + filename, "r")
    if(f.mode == 'r'):
        lines = f.readlines()
        for line in lines:
            wordlist.append(line.strip())

    return wordlist

def brute_force(hashedpass, wordlist):
    choice = input("Select hashing algorithm:\n1. MD5")
    if choice=="1":
        print("running using MD5")
        for word in wordlist:
            hash = hashlib.md5(word.encode('utf-8')).hexdigest()
            if hash == hashedpass:
                print("password: " + word)
                print(hash)
                break

def generate_dictionary(wordlist_address):
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

def main():
    print(generate_dictionary("rockyou-25.txt"))

if __name__ == "__main__":
    main()