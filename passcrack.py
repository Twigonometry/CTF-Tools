import hashlib

def load_wordlist(filename):
    print("Attempting to load word list from /wordlists/" + filename)
    wordlist = list()
    f = open("wordlists/" + filename, "r")
    if(f.mode == 'r'):
        lines = f.readlines()
        for line in lines:
            wordlist.append(line.strip())
    for i in range(0,5):
        print(wordlist[i])

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

def main():
    print("Password cracker, using RockYou wordlist and brute force approach")
    wordlist = load_wordlist("rockyou-75.txt")
    hashedpass = hashlib.md5("password".encode('utf-8')).hexdigest()
    print(hashedpass)
    brute_force(hashedpass, wordlist)

if __name__ == "__main__":
    main()