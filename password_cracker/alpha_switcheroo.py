from string import ascii_lowercase

mangle_map = []

#iterate over letters, adding its lower and uppercase as pairs
for c in ascii_lowercase:
    mangle_map.append("\n(\"" + c + "\", \"" + str(c).upper() + "\")")
    mangle_map.append("\n(\"" + str(c).upper() + "\", \"" + c + "\")")

#write new map to file
with open("mangle_map.txt", "a") as f:
    for pair in mangle_map:
        print(pair)
        f.write(pair)