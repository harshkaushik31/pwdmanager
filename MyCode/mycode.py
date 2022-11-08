import mysql.connector as ms
conn=ms.connect(host='localhost',user='root',passwd='nkr7exfkyg',database='mydb1')
your_value=input("Enter your number ")
if conn.is_connected():
    print('Bhai Connect ho gaya')
mycursor=conn.cursor()
mycursor.execute('select * from pwdmanager')
mydata=mycursor.fetchall()
for i in mydata:
    print(i)
    print(your_value)