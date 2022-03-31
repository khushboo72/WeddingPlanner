import mysql.connector

global __mydb
def server_connection():
    __mydb = None
    if __mydb is None:
        __mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql_123Aqt'
        )
    return __mydb


#function to create database 
def create_database(connection1):    
    cursor=connection1.cursor()
    query="CREATE DATABASE IF NOT EXISTS planner"
    cursor.execute(query)
    connection1.commit()

# def create_data(connection1):    
#     cursor=connection1.cursor()
#     query="CREATE DATABASE IF NOT EXISTS %s;"%('basedata') 
#     cursor.execute(query)
#     connection1.commit()

def get_sql_connection():
    connection1=server_connection()
    create_database(connection1)
    __mydb=None

    if __mydb is None:
        __mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql_123Aqt',
            database='planner'
            )
    return __mydb

#function to create tables in database 
def create_table(connection):
    cursor = connection.cursor()

    create_venue=('''CREATE TABLE IF NOT EXISTS venue(venue_id INT PRIMARY KEY AUTO_INCREMENT,venuename VARCHAR(50) NOT NULL,
            venuetype VARCHAR(20) NOT NULL,venueaddress TEXT,venuecost FLOAT NOT NULL,venuecontact BIGINT,venuelimit INT,venueimage INT)''')
    cursor.execute(create_venue)

    create_mandap=('''CREATE TABLE IF NOT EXISTS mandap(mandap_id INT PRIMARY KEY AUTO_INCREMENT,mandapname VARCHAR(50) NOT NULL,
           mandapdetails TEXT,mandapcost FLOAT NOT NULL,mandapcontact BIGINT,mandapimage INT)''')
    cursor.execute(create_mandap)

    create_meal=('''CREATE TABLE IF NOT EXISTS meal(meal_id INT PRIMARY KEY AUTO_INCREMENT,mealname VARCHAR(50) NOT NULL,mealtype VARCHAR(50),
           mealdetails TEXT,mealcost FLOAT NOT NULL,mealcontact BIGINT )''')
    cursor.execute(create_meal)
    
    create_equipment=('''CREATE TABLE IF NOT EXISTS equipment(equipment_id INT PRIMARY KEY AUTO_INCREMENT,equipmentname VARCHAR(50) NOT NULL,
           equipmentdetails TEXT,equipmentcost FLOAT NOT NULL,equipmentcontact BIGINT)''')
    cursor.execute(create_equipment)
    
    create_decor=('''CREATE TABLE IF NOT EXISTS decor(decor_id INT PRIMARY KEY AUTO_INCREMENT,decorname VARCHAR(50) NOT NULL,
        decordetails TEXT,decorcost FLOAT NOT NULL,decorcontact BIGINT,decorimage INT)''')
    cursor.execute(create_decor)

    create_seating=('''CREATE TABLE IF NOT EXISTS seating(seating_id INT PRIMARY KEY AUTO_INCREMENT,seatingname VARCHAR(50) NOT NULL,
           seatingdetails TEXT,seatingcost FLOAT NOT NULL,seatingcontact BIGINT,seatingimage INT)''')
    cursor.execute(create_seating)

    create_transport=('''CREATE TABLE IF NOT EXISTS transport(transport_id INT PRIMARY KEY AUTO_INCREMENT,transportname VARCHAR(50) NOT NULL,transporttype TEXT,
           transportdetails TEXT,transportcost FLOAT NOT NULL,transportcontact BIGINT)''')
    cursor.execute(create_transport)

    connection.commit()

if __name__ == '__main__':
    connection1= server_connection()
    connection = get_sql_connection()
    #create_table(connection)
    #create_data(connection1) 