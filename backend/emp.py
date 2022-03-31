import mysql.connector
from DBHelper import get_sql_connection
from flask import request

def get_emp(connection):  # to display employee working in a comnpany 
    cursor = connection.cursor()
    query = ("SELECT * FROM employee")
    cursor.execute(query)
    response = []
    for (emp_id, empname,empemail,empcontact,empusername,emppassword) in cursor:
        response.append({'emp_id': emp_id,
                        'empname': empname,
                         'empemail': empemail,
                         'empcontact': empcontact,
                         'empusername': empusername,
                        'emppassword': emppassword
                         })
    return response

def insert_emp(connection,emps):     
    cursor = connection.cursor()    
    query = ("INSERT INTO employee(empname,empemail,empcontact,,empusername,emppassword) VALUES (%s,%s,%s,%s,%s)")
    data = ( emps['empname'],emps['empemail'],emps['empcontact'],emps['empusername'],emps['emppassword'])
    cursor.execute(query, data)
    connection.commit()
   # return cursor.lastrowid


def delete_emp(connection,emp_id):
    cursor = connection.cursor()
    query = ("DELETE FROM employee WHERE emp_id="+str(emp_id))
    cursor.execute(query)
    connection.commit()


def update_emp(connection,emps):
    cursor = connection.cursor()
    query = ("UPDATE employee SET empname=%s, empemail=%s, empcontact=%s" " WHERE emp_id=%s")
    data = ( emps['empname'],emps['empemail'],emps['empcontact'], emps['emp_id'],emps['empusername'],emps['emppassword'])                             
    cursor.execute(query,data)
    connection.commit()


if __name__ == '__main__':
    connection = get_sql_connection()
    #print(get_emp(connection))
    print(insert_emp(connection, {  
        'empname': 'Jenish',
        'empemail': 'jenish@gmail.com',
        'empcontact':'975312314',
         'empusername': 'jenish',
          'emppassword': 'jenish'
    }))
    #print(delete_emp(connection, 3))
     
    # print(update_emp(connection, {
    #     'emp_id':'2',
    #      'empname': 'Rajeev',
    #      'empemail': 'rajeev@gmail.com',
    #      'empcontact':'8987514202'
    #    'empusername': rajeev,
    #     'emppassword': rajeev

    #     }))

