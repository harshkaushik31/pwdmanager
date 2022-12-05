# Password Manager

master_pwd="nkr7exfkyg"
passw = input('Please provide the master password to start using Password Manager: ')

if passw == master_pwd:
    print('You\'re in')
else:
    print('Sorry Wrong Password!')
    exit() 


#importing the connectors and establishing the connection
import mysql.connector as ms
conn=ms.connect(host='localhost',user='root',passwd='nkr7exfkyg', database='mydb1')
if conn.is_connected():
    print("Connected Sucessfully...")
my_cursor=conn.cursor()

#hash_key    
hash_key={'a':'z','b':'y','c':'x','d':'w',
        'e':'v','f':'u','g':'t','h':'s',
        'i':'r','j':'q','k':'p','l':'o',
        'm':'n',
        'n':'m','o':'l','p':'k','q':'j',
        'r':'i','s':'h','t':'g','u':'f',
        'v':'e','w':'d','x':'c','y':'b',
        'z':'a',
        'A':'Z','B':'Y','C':'X','D':'W',
        'E':'V','F':'U','G':'T','H':'S',
        'I':'R','J':'Q','K':'P','L':'O',
        'M':'N',
        'N':'M','O':'L','P':'K','Q':'J',
        'R':'I','S':'H','T':'G','U':'F',
        'V':'E','W':'D','X':'C','Y':'B',
        'Z':'A',
        '!':'*','@':'&','#':'^','$':'%',
        '%':'$','^':'#','&':'@','*':'!'}

# hasher            
def hasher(password):
    new_pass=""
    for i in password:
        new_pass+=hash_key[i]
    return new_pass



# creating all the functions
def menu():
    print("-"*120)
    print(('-'*33) + 'Menu'+ ('-' *33))
    print('1. Create new password')
    print('2. Find all sites and apps connected to an email')
    print('3. Find a password for a site or app')
    print('4. Update password for a existing site or app')
    print('5. Delete password for a existing site or app')
    print('Q. Exit')
    print("-"*120)
    print()
    return input(': ')

def create():
    print('Please provide the name of the site or app you want to generate a password for: ')
    app_name = input()
    print('Please provide a password for this site or app: ')
    plain_pwd = input()
    passwd = hasher(plain_pwd)
    user_email = input('Please provide a user email for this site or app: ')
    username = input('Please provide a username for this site or app (if applicable): ')
    if username == None:
        username = ''
    query = "INSERT INTO pwdmanager (app_name,email,password,username) VALUES ('{}','{}','{}','{}')".format(app_name,user_email,passwd,username)
    my_cursor.execute(query)
    conn.commit()
    print("Record Inserted...")


def find_accounts():
    print('Please provide the email that you want to find accounts for')
    user_email = input()
    query = "SELECT * FROM pwdmanager WHERE email='{}'".format(user_email,)
    my_cursor.execute(query)
    my_data=my_cursor.fetchall()
    if my_data!=[]:
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
        print("|","-"*10,"app_name","-"*10,"|","-"*11,"e-mail","-"*11,"|","-"*10,"password","-"*10,"|","-"*10,"username","-"*10,"|")
        for row in my_data:
            print("|","%30s"%row[0],"|","%30s"%row[1],"|","%30s"%hasher(row[2]),"|","%30s"%row[3],"|")
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
    else:
        print("Wrong data input!")
   


def  find():
    print('Please provide the name of the site or app you want to find the password to')
    app_name = input()
    query = "SELECT * FROM pwdmanager WHERE app_name='{}'".format(app_name,)
    my_cursor.execute(query)
    my_data = my_cursor.fetchall()
    if my_data!=[]:
        print("+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+-","-"*28,"-+")
        print("|","-"*10,"app_name","-"*10,"|","-"*11,"e-mail","-"*11,"|","-"*10,"password","-"*10,"|","-"*10,"username","-"*10,"|")
        for row in my_data:
            print("|","%30s"%row[0],"|","%30s"%row[1],"|","%30s"%hasher(row[2]),"|","%30s"%row[3],"|")
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
    query="UPDATE pwdmanager SET password='{}' WHERE app_name='{}' AND username='{}'".format(hashed_new_pwd,app_name,username)
    my_cursor.execute(query)
    conn.commit()
    print("Record Updated Sucessfully...")

def delete():
    print("Please enter the app/site name which you want to delete password for: ")
    app_name=input()
    print("Please enter the username of ",app_name," for which you want to delete your password: ")
    username=input()
    query="DELETE FROM pwdmanager WHERE app_name='{}' AND username='{}'".format(app_name,username)
    my_cursor.execute(query)
    conn.commit()
    print("Record Deleted Sucessfully...")
    
        
 
choice = menu()


while True:
    if choice == '1':
        create()
    elif choice == '2':
        find_accounts()
    elif choice == '3':
        find()
    elif choice == '4':
        update()
    elif choice == '5':
        delete()
    elif choice == 'Q':
        exit(0)
    choice = menu()