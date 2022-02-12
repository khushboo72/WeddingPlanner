import mysql.connector
from DBHelper import get_sql_connection

def get_mandap(connection): # to display mandap table 
    
    cursor = connection.cursor()
    query = ("SELECT * FROM mandap")

    cursor.execute(query)

    response = []
    for (mandap_id, mandapname,mandapdetails,mandapcost,mandapcontact,mandapimage) in cursor:
        response.append({'mandap_id': mandap_id,
                        'mandapname': mandapname,
                         'mandapdetails': mandapdetails,
                         'mandapcost': mandapcost,
                         'mandapcontact': mandapcontact,
                         'mandapimage': mandapimage,
                         })

    return response


def insert_mandap(connection,mandaps): # to insert values in mandap table 
  
    cursor = connection.cursor()
    query = ("INSERT INTO mandap(mandapname,mandapdetails,mandapcost,mandapcontact,mandapimage) VALUES (%s,%s,%s,%s,%s)")
    data = ( mandaps['mandapname'], mandaps['mandapdetails'],
            mandaps['mandapcost'], mandaps['mandapcontact'],mandaps['mandapimage'])
    cursor.execute(query, data)
    connection.commit()
    #return cursor.lastrowid


def delete_mandap(connection, mandap_id): #to delete data from mandap table 
    cursor = connection.cursor()
    query = ("DELETE FROM mandap WHERE mandap_id="+str(mandap_id))
    cursor.execute(query)
    connection.commit()

def update_mandap(connection,mandaps):
    cursor = connection.cursor()
    query = ("UPDATE mandap SET mandapname=%s,mandapdetails=%s, mandapcost=%s,mandapcontact=%s,mandapimage=%s"
             " WHERE mandap_id=%s")
    data = (mandaps['mandapname'], mandaps['mandapdetails'],
            mandaps['mandapcost'], mandaps['mandapcontact'],mandaps['mandapimage'],mandaps['mandap_id'])                             
    cursor.execute(query,data)
    connection.commit()

if __name__ == '__main__':
    connection = get_sql_connection()
     
    # print(update_mandap(connection, {
    #     'mandap_id':'3',
    #     'mandapname':'Dome Shaped Mandap',
    #     'mandapdetails':'Mandap has exquisite pillars showing the elite wedding',
    #     'mandapcost':'2500.75',
    #     'mandapcontact':'9995345678',
    #     'mandapimage':'5'
    #     }))

