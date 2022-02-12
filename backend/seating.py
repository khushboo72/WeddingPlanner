import mysql.connector
from DBHelper import get_sql_connection


def get_seating(connection): 

    cursor = connection.cursor()
    query = ("SELECT * FROM seating")
    cursor.execute(query)

    response = []
    for (seating_id, seatingname,seatingdetails,seatingcost,seatingcontact,seatingimage) in cursor:
        response.append({'seating_id': seating_id,
                        'seatingname': seatingname,
                         'seatingdetails': seatingdetails,
                         'seatingcost': seatingcost,
                         'seatingcontact': seatingcontact,
                         'seatingimage':seatingimage 
                         })
    return response

def insert_seating(connection,seatings): 

    cursor = connection.cursor()
    query = ("INSERT INTO seating( seatingname,seatingdetails,seatingcost,seatingcontact,seatingimage) VALUES (%s,%s,%s,%s,%s)")
    data = (seatings['seatingname'], seatings['seatingdetails'],
            seatings['seatingcost'], seatings['seatingcontact'],seatings['seatingimage'])
    cursor.execute(query, data)
    connection.commit()
    # return cursor.lastrowid


def delete_seating(connection, seating_id): 
    cursor = connection.cursor()
    query = ("DELETE FROM seating WHERE seating_id="+str(seating_id))
    cursor.execute(query)
    connection.commit()


def update_seating(connection, seatings):
    cursor = connection.cursor()
    query = ("UPDATE seating SET seatingname=%s, seatingdetails=%s, seatingcost=%s,seatingcontact=%s,seatingimage=%s"
             " WHERE seating_id=%s")
    data = (seatings['seatingname'], seatings['seatingdetails'],
            seatings['seatingcost'], seatings['seatingcontact'],seatings['seatingimage'],seatings['seating_id'])                             
    cursor.execute(query,data)
    connection.commit()

    # return stage['stage_id']


if __name__ == '__main__':
    connection = get_sql_connection()
    #print(get_seating(connection))
    # print(insert_seating(connection, {  
    #     'seatingname': 'Lounge Style Seating',
    #     'seatingdetails': 'includes sofas and coffee tables',
    #     'seatingcost': '8500.78',
    #     'seatingcontact': '7892233273',
    #     'seatingimage': '0'
    # }))
    #print(delete_seating(connection, 3))
     
    # print(update_seating(connection, {
    #     'seating_id':'2',
    #     'seatingname': 'Divan Style Seating ',
    #     'seatingdetails': 'bright colours and the Indian-ness of the seating style',
    #     'seatingcost': '4500.78',
    #     'seatingcontact': '8998233273',
    #     'seatingimage': '0'
    #     }))
