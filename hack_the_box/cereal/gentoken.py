import jwt

#take key from old git code - commit ID 8f2a1a88f15b9109e1f63e4e4551727bfb38eee5
key = "secretlhfIH&FY*#oysuflkhskjfhefesf"

#encode with HMAC-SHA-256
encoded = jwt.encode({"some": "payload"}, key, algorithm="HS256")

print(encoded)
