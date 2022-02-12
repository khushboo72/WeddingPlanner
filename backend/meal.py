import mysql.connector
from DBHelper import get_sql_connection


def get_meal(connection):  # to display meal table
    cursor = connection.cursor()
    query = ("SELECT * FROM meal")
    cursor.execute(query)
    response = []
    for (meal_id, mealname, mealtype, mealdetails, mealcost, mealcontact) in cursor:
        response.append({'meal_id': meal_id,
                        'mealname': mealname,
                         'mealtype': mealtype,
                         'mealdetails': mealdetails,
                         'mealcost': mealcost,
                         'mealcontact': mealcontact
                         })
    return response


def insert_meal(connection, meals):  # to insert values in meal table
    cursor = connection.cursor()
    query = ("INSERT INTO meal( mealname,mealtype,mealdetails,mealcost,mealcontact) VALUES (%s,%s,%s,%s,%s)")
    data = (meals['mealname'], meals['mealtype'], meals['mealdetails'],
            meals['mealcost'], meals['mealcontact'])
    cursor.execute(query, data)
    connection.commit()
    # return cursor.lastrowid


def delete_meal(connection, meal_id):  # to delete data from meal table
    cursor = connection.cursor()
    query = ("DELETE FROM meal WHERE meal_id="+str(meal_id))
    cursor.execute(query)
    connection.commit()


def update_meal(connection,meals):
    cursor = connection.cursor()
    query = ("UPDATE meal SET mealname=%s,mealtype=%s, mealdetails=%s, mealcost=%s,mealcontact=%s"
             " WHERE meal_id=%s")
    data = (meals['mealname'], meals['mealtype'], meals['mealdetails'],
            meals['mealcost'], meals['mealcontact'],meals['meal_id'])                             
    cursor.execute(query,data)
    connection.commit()


if __name__ == '__main__':
    connection = get_sql_connection()

    # print(update_meal(connection, {
    #     'meal_id':'2',
    #     'mealname':'Gujarati',
    #     'mealtype':'Breakfast',
    #     'mealdetails':'1 plate will include khaman,jalebi',
    #     'mealcost':'.75',
    #     'mealcontact':'8965345678'
    #     }))


