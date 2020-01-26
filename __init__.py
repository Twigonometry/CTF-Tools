import hashlib

def load_wordlist(filename):
    print("Attempting to load word list from /wordlists/", filename)
    wordlist = list()
    f = open("wordlists/" + filename, "r")
    if(f.mode == 'r'):
        lines = f.readlines()
        for line in lines:
            wordlist.append(line)
    for i in range(0,5):
        print(wordlist[i])

def main():
    print("Password cracker, using RockYou wordlist and brute force approach")
    load_wordlist("rockyou-75.txt")

if __name__ == "__main__":
    main()