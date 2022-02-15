import mysql.connector
from DBHelper import get_sql_connection
from DBHelper import server_connection


def create_databaseadmin(connection1):    
    cursor=connection1.cursor()
    query="CREATE DATABASE IF NOT EXISTS admin"
    cursor.execute(query)
    connection1.commit()

def admin_connection():
    connection1=server_connection()
    create_databaseadmin(connection1)
    __mydb=None

    if __mydb is None:
        __mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql_123Aqt',
            database='admin'
            )
    return __mydb

def create_tableadmin(connection2):
    cursor = connection2.cursor()
    create_accounts=('''CREATE TABLE IF NOT EXISTS accounts(user_id INT PRIMARY KEY AUTO_INCREMENT,usertype VARCHAR(20) NOT NULL,username VARCHAR(50) NOT NULL,
            userpassword VARCHAR(20) NOT NULL,email varchar(40)NOT NULL,usercontact BIGINT NOT NULL)''')
    cursor.execute(create_accounts)


def register(connection2,account):
    cursor=connection2.cursor()
    query = ("INSERT INTO accounts(username,usertype,userpassword,email,usercontact) VALUES (%s,%s,%s,%s,%s)")
    data = ( account['username'],account['usertype'], account['userpassword'],account['email'],account['usercontact'])
    cursor.execute(query, data)
    connection2.commit()


#fuction to update user(event planner) details in accounts table 
def update_account(connection2,account):
    cursor = connection2.cursor()
    query = ("UPDATE accounts SET username=%s,userpassword=%s,email=%s,usercontact=%s" " WHERE user_id=%s")
    data = (account['username'], account['userpassword'],account['email'],account['usercontact'])                             
    cursor.execute(query,data)
    connection2.commit()


def delete_account(connection2, user_id):
    cursor = connection2.cursor()
    query = ("DELETE FROM accounts WHERE user_id="+str(user_id))
    cursor.execute(query)
    connection2.commit()


if __name__ == '__main__':
    connection1= server_connection()
    connection= get_sql_connection()
    connection2=admin_connection()
    print(register(connection2,{
        'username':'Rashi',
        'userpassword':'rashi',
        'email':'rashi@gmail.com',
        'usercontact': '9099716655'
    }))
    # print(delete_account(connection,3))
