import mysql.connector as ms
conn=ms.connect(host='localhost',user='root',passwd='nkr7exfkyg', database='mydb1')
if conn.is_connected():
    print('connected')