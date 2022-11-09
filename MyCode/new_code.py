# Password Manager

master_pwd="nkr7exfkyg"
passw = input('Please provide the master password to start using pwdmanager: ')

if passw == master_pwd:
    print('You\'re in')
else:
    print('no luck')
    exit() 


#importing the connectors and establishing the connection
import mysql.connector as ms
conn=ms.connect(host='localhost',user='root',passwd='nkr7exfkyg', database='mydb1')
if conn.is_connected():
    print("\033[92m {}\033[00m".format("Connected Sucessfully"))
my_cursor=conn.cursor()

# printing in green
def pr_green(str):
    print("\033[92m {}\033[00m" .format(str))

# prining in red
def pr_red(str): 
    print("\033[91m {}\033[00m" .format(str))

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
    pr_green("-"*120)
    print(('-'*33) + 'Menu'+ ('-' *33))
    print('1. Create new password')
    print('2. Find all sites and apps connected to an email')
    print('3. Find a password for a site or app')
    print('4. Update password for a existing site or app')
    print('5. Delete password for a existing site or app')
    print('Q. Exit')
    pr_green("-"*120)
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
    pr_green("Record Inserted...")


def find_accounts():
    print('Please proivide the email that you want to find accounts for')
    user_email = input()
    query = "SELECT * FROM pwdmanager WHERE email=%s"
    value=(user_email,)
    my_cursor.execute(query,value)
    my_data=my_cursor.fetchall()
    if my_data!=None:
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
        print("|","-"*10,"app_name","-"*10,"|","-"*11,"e-mail","-"*11,"|","-"*10,"password","-"*10,"|","-"*10,"username","-"*10,"|")
        for row in my_data:
            print("|","%30s"%row[0],"|","%30s"%row[1],"|","%30s"%unhasher(row[2]),"|","%30s"%row[3],"|")
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
    else:
        print("Wrong data input!")
   


def  find():
    print('Please provide the name of the site or app you want to find the password to')
    app_name = input()
    query = "SELECT * FROM pwdmanager WHERE app_name=%s"
    value = (app_name,)
    my_cursor.execute(query,value)
    my_data = my_cursor.fetchall()
    if my_data!=None:
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
        print("|","-"*10,"app_name","-"*10,"|","-"*11,"e-mail","-"*11,"|","-"*10,"password","-"*10,"|","-"*10,"username","-"*10,"|")
        for row in my_data:
            print("|","%30s"%row[0],"|","%30s"%row[1],"|","%30s"%unhasher(row[2]),"|","%30s"%row[3],"|")
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
    
    else:
        print("Wrong app or site name")
   

def update():
    print("Please enter the app/site name which you want to update password for: ")
    app_name=input()
    print("Please enter the username of ",app_name," for which you want to upadate your password: ")
    username=input()
    print("Enter new Password: ")
    new_pass=input()
    hashed_new_pwd=hasher(new_pass)
    query="UPDATE pwdmanager SET password=%s WHERE app_name=%s AND username=%s"
    value=(hashed_new_pwd,app_name,username)
    my_cursor.execute(query,value)
    conn.commit()
    pr_green("Record Updated Sucessfully...")

def delete():
    print("Please enter the app/site name which you want to delete password for: ")
    app_name=input()
    print("Please enter the username of ",app_name," for which you want to delete your password: ")
    username=input()
    query="DELETE FROM pwdmanager WHERE app_name=%s AND username=%s"
    value=(app_name,username)
    my_cursor.execute(query,value)
    conn.commit()
    pr_green("Record Deleted Sucessfully...")
    # exit()
        
 
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
        pr_red("Error calling again and again...")
    else:
        choice = menu()
exit()