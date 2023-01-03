import mysql.connector

conn=mysql.connector.connect(host="localhost",user="root",password="ch381144",database="facial_recognition", auth_plugin='mysql_native_password', )
print(conn)