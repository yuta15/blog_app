import bcrypt


pw = "test123"
hashed_pw = bcrypt.hashpw(password=pw.encode('utf-8'), salt=bcrypt.gensalt())
print(hashed_pw)

print(bcrypt.checkpw(pw.encode('utf-8'), hashed_pw))
