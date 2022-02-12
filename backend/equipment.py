import mysql.connector
from DBHelper import get_sql_connection


def get_equipment(connection): 

    cursor = connection.cursor()
    query = ("SELECT * FROM equipment")
    cursor.execute(query)
    response = []
    for (equipment_id, equipmentname,equipmentdetails,equipmentcost,equipmentcontact) in cursor:
        response.append({'equipment_id': equipment_id,
                        'equipmentname': equipmentname,
                         'equipmentdetails': equipmentdetails,
                         'equipmentcost': equipmentcost,
                         'equipmentcontact': equipmentcontact 
                         })
    return response

def insert_equipment(connection,equipments): 

    cursor = connection.cursor()
    query = ("INSERT INTO equipment(equipmentname,equipmentdetails,equipmentcost,equipmentcontact) VALUES (%s,%s,%s,%s)")
    data = (equipments['equipmentname'], equipments['equipmentdetails'],
            equipments['equipmentcost'], equipments['equipmentcontact'])
    cursor.execute(query, data)
    connection.commit()
    # return cursor.lastrowid


def delete_equipment(connection, equipment_id): 
    cursor = connection.cursor()
    query = ("DELETE FROM equipment WHERE equipment_id="+str(equipment_id))
    cursor.execute(query)
    connection.commit()

def update_equipment(connection, equipments):
    cursor = connection.cursor()
    query = ("UPDATE equipment SET equipmentname=%s, equipmentdetails=%s, equipmentcost=%s,equipmentcontact=%s"
             " WHERE equipment_id=%s")
    data = (equipments['equipmentname'], equipments['equipmentdetails'],
            equipments['equipmentcost'], equipments['equipmentcontact'],equipments['equipment_id'])                             
    cursor.execute(query,data)
    connection.commit()



if __name__ == '__main__':
    connection = get_sql_connection()



# print(update_equipment(connection, {
#         'equipment_id':'3',
#         'equipmentname':'Speakers',
#         'equipmentdetails':'High quality speakers',
#         'equipmentcost':'700.75',
#         'equipmentcontact':'9785345678'
#         }))

