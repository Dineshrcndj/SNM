import mysql.connector 
# app.secret_key='dineshkey'
# user_data={'dinesh':{'email':'dinesh.rcnd@gmail.com','password':'123'}}
userdata={}
mydb=mysql.connector.connect(user='root',host='localhost',password='admin',db='snmp') #Mysql connection
cursor=mydb.cursor()
a=cursor.execute('select username from users where email="dinesh.rcnd1@gmail.com"')
mydb.commit()
print(a)
cursor.close()