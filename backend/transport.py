import mysql.connector
from DBHelper import get_sql_connection

def get_transport(connection):

    cursor = connection.cursor()
    query = ("SELECT * FROM transport")
    cursor.execute(query)
    response = []
    for (transport_id, transportname,transporttype,transportdetails,transportcost ,transportcontact) in cursor:
        response.append({'transport_id': transport_id,
                        'transportname': transportname,
                         'transporttype': transporttype,
                         'transportdetails': transportdetails,
                         'transportcost': transportcost,
                         'transportcontact': transportcontact

                         })

    return response

def insert_transport(connection,transports):
  
    cursor = connection.cursor()
    query = ("INSERT INTO transport(transportname,transporttype,transportdetails,transportcost ,transportcontact) VALUES (%s,%s,%s,%s,%s)")
    data = ( transports['transportname'],transports['transporttype'],transports['transportdetails'],
            transports['transportcost'], transports['transportcontact'])
    cursor.execute(query, data)
    connection.commit()
   # return cursor.lastrowid


def delete_transport(connection, transport_id):
    cursor = connection.cursor()
    query = ("DELETE FROM transport WHERE transport_id="+str(transport_id))
    cursor.execute(query)
    connection.commit()


def update_transport(connection,transports):
    cursor = connection.cursor()
    query = ("UPDATE transport SET transportname=%s, transporttype=%s, transportdetails=%s,transportcost=%s,transportcontact=%s"
             " WHERE transport_id=%s")
    data = ( transports['transportname'],transports['transporttype'],transports['transportdetails'],
            transports['transportcost'], transports['transportcontact'], transports['transport_id'])                             
    cursor.execute(query,data)
    connection.commit()



if __name__ == '__main__':
    connection = get_sql_connection()
    #print(get_transport(connection))
    print(insert_transport(connection, {  
        'transportname': 'Yahi Travels',
        'transporttype': 'Car',
        'transportdetails':'BMW',
        'transportcost': '5500',
        'transportcontact':'6727263633'

    }))
    #print(delete_transport(connection, 3))
     
    # print(update_transport(connection, {
    #     'transport_id':'2',
    #     'transportname': 'Soha Travels',
    #     'transporttype': 'car',
    #     'transportdetails':'wedding car',
    #     'transportcost': '7800',
    #     'transportcontact':'8966272727'

    #     }))
