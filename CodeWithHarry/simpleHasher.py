hash_key = (('s', '$'), ('and', '&'), 
            ('a', '@'), ('o', '0'), ('i', '1'),
            ('I', '|'))

def hasher(password):
    for a,b in hash_key:
        password = password.replace(a, b)
    return password


password = input("Enter your password\n")
password = hasher(password)
print("Your secure password is ",password)

unhash_key = (('$', 's'), ('&', 'and'), 
            ('@', 'a'), ('0', 'o'), ('1', 'i'),
            ('|', 'I'))
def unhasher(hashed_password):
    for a,b in unhash_key:
        hashed_password = hashed_password.replace(a, b)
    return hashed_password

password = input("Enter your password\n")
password = unhasher(password)
print("Your secure password is ",password)
