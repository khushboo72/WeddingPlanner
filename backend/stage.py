import mysql.connector
from DBHelper import get_sql_connection


def get_stage(connection): 

    cursor = connection.cursor()
    query = ("SELECT * FROM stage")

    cursor.execute(query)

    response = []
    for (stage_id, stagename,stagedetails,stagecost,stagecontact,stageimage) in cursor:
        response.append({'stage_id': stage_id,
                        'stagename': stagename,
                         'stagedetails': stagedetails,
                         'stagecost': stagecost,
                         'stagecontact': stagecontact,
                         'stageimage':stageimage 
                         })

    return response

def insert_stage(connection,stages): 

    cursor = connection.cursor()
    query = ("INSERT INTO stage( stagename,stagedetails,stagecost,stagecontact,stageimage) VALUES (%s,%s,%s,%s,%s)")
    data = (stages['stagename'], stages['stagedetails'],
            stages['stagecost'], stages['stagecontact'],stages['stageimage'])
    cursor.execute(query, data)
    connection.commit()
    # return cursor.lastrowid


def delete_stage(connection, stage_id): 
    cursor = connection.cursor()
    query = ("DELETE FROM stage WHERE stage_id="+str(stage_id))
    cursor.execute(query)
    connection.commit()


def update_stage(connection, stages):
    cursor = connection.cursor()
    query = ("UPDATE stage SET stagename=%s, stagedetails=%s, stagecost=%s,stagecontact=%s,stageimage=%s"
             " WHERE stage_id=%s")
    data = (stages['stagename'], stages['stagedetails'], stages['stagecost'],stages['stagecontact'],stages['stageimage'],stages['stage_id'])                             
    cursor.execute(query,data)
    connection.commit()

    # return stage['stage_id']


if __name__ == '__main__':
    connection = get_sql_connection()
    
    # print(update_stage(connection, {
    #     'stage_id':'2',
    #     'stagename':'Traditional Style',
    #     'stagedetails':'Diyas,candles,flowers will be used to decorate the stage',
    #     'stagecost':'4500.75',
    #     'stagecontact':'8965345678',
    #     'stageimage':'56'
    #     }))



