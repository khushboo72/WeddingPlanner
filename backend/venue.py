import mysql.connector
from DBHelper import get_sql_connection

# def convertToBinary(filename):
#     with open(filename,'rb') as file:
#         binarydata=file.read()
#     return binarydata
# def convertToFile(binarydata,filename):
#     with open(filename,'wb') as file:
#         file.write(binarydata)

#global venue_id
def get_venue(connection):

    cursor = connection.cursor()
    query = ("SELECT * FROM venue")

    cursor.execute(query)

    response = []
    for (venue_id, venuename,venuetype, venueaddress, venuecost, venuecontact,venuelimit, venueimage) in cursor:
        response.append({'venue_id': venue_id,
                        'venuename': venuename,
                         'venuetype': venuetype,
                         'venueaddress': venueaddress,
                         'venuecost': venuecost,
                         'venuecontact': venuecontact,
                         'venuelimit':venuelimit,
                         'venueimage': venueimage,
                         })

    return response


def insert_venue(connection,venues):
  
    cursor = connection.cursor()
    query = ("INSERT INTO venue(venuename,venuetype,venueaddress,venuecost,venuecontact,venuelimit,venueimage) VALUES (%s,%s,%s,%s,%s,%s,%s)")
    # convertPic=convertToFile ("C:\Users\Admin\Pictures\Screenshots\ ave.jpg")
    data = ( venues['venuename'],venues['venuetype'],venues['venueaddress'],
            venues['venuecost'], venues['venuecontact'],venues['venuelimit'] , venues['venueimage'])
    cursor.execute(query, data)
    connection.commit()
   # return cursor.lastrowid


def delete_venue(connection, venue_id):
    cursor = connection.cursor()
    query = ("DELETE FROM venue WHERE venue_id="+str(venue_id))
    cursor.execute(query)
    connection.commit()


def update_venue(connection, venues):
    cursor = connection.cursor()
    query = ("UPDATE venue SET venuename=%s, venuetype=%s, venueaddress=%s,venuecost=%s,venuecontact=%s,venuelimit=%s,venueimage=%s"
             " WHERE venue_id=%s")
    data = ( venues['venuename'],venues['venuetype'],venues['venueaddress'],
            venues['venuecost'], venues['venuecontact'],  venues['venueimage'],venues['venuelimit'], venues['venue_id'])                             
    cursor.execute(query,data)
    connection.commit()



if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_venue(connection))
    # print(insert_venue(connection, {  
    #     'venuename': 'Paradise Farms',
    #     'venueaddress': 'Adajan Main Road,Vapi ',
    #     'venuecost': '89439.44',
    #     'venuecontact': '9874538473',
    #     'venuetype': 'outdoor',
    #      'venuelimit':'800',
    #     'venueimage': '8'
    # }))
    # print(delete_venue(connection, 27))
     
    # print(update_venue(connection, {
    #     'venue_id':'26',
    #     'venuename': 'Jolly Party Plot',
    #     'venueaddress': 'Pooja Complex, Citylight Main Road,Surat ',
    #     'venuecost': '69439.44',
    #     'venuecontact': '8542238473',
    #     'venuetype': 'outdoor',
    #     'venueimage': '77'
    #     }))
