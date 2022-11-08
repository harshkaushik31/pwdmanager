# Password Manager

#importing the connectors and establishing the connection
import mysql.connector as ms
conn=ms.connect(host='localhost',user='root',passwd='nkr7exfkyg', database='mydb1')
if conn.is_connected():
    print("\033[92m {}\033[00m" .format("Connected Sucessfully"))
my_cursor=conn.cursor()

#hash_key    
hash_key = (('s', '$'), ('and', '&'), 
            ('a', '@'), ('o', '0'), ('i', '1'),
            ('I', '|'))

# hasher            
def hasher(password):
    for a,b in hash_key:
        password = password.replace(a, b)
    return password

#unhash_key
unhash_key = (('$', 's'), ('&', 'and'), 
            ('@', 'a'), ('0', 'o'), ('1', 'i'),
            ('|', 'I'))

#unhasher
def unhasher(hashed_password):
    for a,b in unhash_key:
        hashed_password = hashed_password.replace(a, b)
    return hashed_password


# menu
def menu():
    print('-'*70)
    print(('-'*33) + 'Menu'+ ('-' *33))
    print('1. Create new password')
    print('2. Find all sites and apps connected to an email')
    print('3. Find a password for a site or app')
    print('4. Update password for a existing site or app')
    print('5. Delete password for a existing site or app')
    print('Q. Exit')
    print('-'*70)
    return input(': ')

def create():
    print('Please proivide the name of the site or app you want to generate a password for: ')
    app_name = input()
    print('Please provide a password for this site: ')
    plain_pwd = input()
    passwd = hasher(plain_pwd)
    user_email = input('Please provide a user email for this app or site: ')
    username = input('Please provide a username for this app or site (if applicable): ')
    if username == None:
        username = ''
    query = "INSERT INTO pwdmanager (app_name,email,password,username) VALUES (%s,%s,%s,%s)"
    values=(app_name,user_email,passwd,username)
    my_cursor.execute(query,values)
    conn.commit()
    print("Record Inserted...")


def find_accounts():
    return 1


def  find():
    return 1

def update():
    return 1

def delete():
    return 1

choice = menu()

while choice != 'Q':
    if choice == '1':
        create()
    if choice == '2':
        find_accounts()
    if choice == '3':
        find()
    if choice == '4':
        update()
    if choice == '5':
        delete()
    else:
        choice = menu()
exit()
