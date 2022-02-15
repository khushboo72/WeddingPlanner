import mysql.connector
from DBHelper import get_sql_connection


def insert_booking(connection, customerdetails):
    cursor = connection.cursor()

    # insert customer details
    cust_query = ("INSERT INTO customerdetails(custname,custcontact,custemail,custaddress,eventtype) VALUES (%s,%s,%s,%s,%s)")
    cust_data = (customerdetails['custname'], customerdetails['custcontact'],
    customerdetails['custemail'], customerdetails['custaddress'], customerdetails['eventtype'])
    cursor.execute(cust_query, cust_data)
    cust_id = cursor.lastrowid
    connection.commit()

    #bill_id = cursor.lastrowid
    # insert equipmentdetails
    equipment_query = ( "INSERT INTO equipmentdetails (cust_id,equipment_id,quantity,totalprice) VALUES (%s,%s,%s,%s)")
    equipment_data = []
    for equipment_detail in customerdetails['equipmentdetails']:
        equipment_data.append([
            cust_id,
            int(equipment_detail['equipment_id']),
            float(equipment_detail['quantity']),
            float(equipment_detail['totalprice'])
        ])

    cursor.executemany(equipment_query, equipment_data)
    connection.commit()
    return cust_id


# function to delete an booking 
def delete_booking(connection,cust_id):  
    cursor = connection.cursor()
    query = ("DELETE customerdetails,eventdetails FROM customerdetails INNER JOIN eventdetails ON customerdetails.cust_id=eventdetails.cust_id AND customerdetails.cust_id="+str(cust_id))
    cursor.execute(query)
    connection.commit()


if __name__ == '__main__':
    connection = get_sql_connection()
    # print(insert_customerdetails(connection,{
    #     'cust_id': 'cust_id',
    #     'custname': 'empty cust',
    #     'custcontact': '7837328273',
    #     'custemail': 'empty@gmail.com',
    #     'custaddress': 'Priyansh Tower,Citylight,Surat',
    #     'eventtype': 'Wedding',
    #     'equipmentdetails': [
    #         {
    #             'equipment_id': '1',
    #             'quantity': '1',
    #             'totalprice': '60'
    #         },
    #         {
    #             'equipment_id': '3',
    #             'quantity': '3',
    #             'totalprice': '90'
    #         }
    #     ]
        
    # }))
   # print(delete_booking(connection,2))
