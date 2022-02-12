import mysql.connector
from DBHelper import get_sql_connection


def get_decor(connection): 

    cursor = connection.cursor()
    query = ("SELECT * FROM decor")

    cursor.execute(query)

    response = []
    for (decor_id, decorname,decordetails,decorcost,decorcontact,decorimage) in cursor:
        response.append({'decor_id': decor_id,
                        'decorname': decorname,
                         'decordetails': decordetails,
                         'decorcost': decorcost,
                         'decorcontact': decorcontact,
                         'decorimage':decorimage 
                         })

    return response

def insert_decor(connection,decors): 

    cursor = connection.cursor()
    query = ("INSERT INTO decor( decorname,decordetails,decorcost,decorcontact,decorimage) VALUES (%s,%s,%s,%s,%s)")
    data = (decors['decorname'], decors['decordetails'],
            decors['decorcost'], decors['decorcontact'],decors['decorimage'])
    cursor.execute(query, data)
    connection.commit()
    # return cursor.lastrowid


def delete_decor(connection, decor_id): 
    cursor = connection.cursor()
    query = ("DELETE FROM decor WHERE decor_id="+str(decor_id))
    cursor.execute(query)
    connection.commit()

def update_decor(connection, decors):
    cursor = connection.cursor()
    query = ("UPDATE decor SET decorname=%s, decordetails=%s, decorcost=%s,decorcontact=%s,decorimage=%s"
             " WHERE decor_id=%s")
    data = (decors['decorname'], decors['decordetails'],
            decors['decorcost'], decors['decorcontact'],decors['decorimage'],decors['decor_id'])                             
    cursor.execute(query,data)
    connection.commit()


if __name__ == '__main__':
    connection = get_sql_connection()
    

# print(update_decor(connection, {
#         'decor_id':'1',
#         'decorname':'Vintage Style',
#         'decordetails':'antique looking decor',
#         'decorcost':'1200.75',
#         'decorcontact':'8985345678',
#         'decorimage':'6'
#         }))

