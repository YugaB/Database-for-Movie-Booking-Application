import server

def deleteSeattatus(userID, showID, showTime):
    print('Inside model - deleteSeattatus', userID, showID, showTime)
    d = server.mysql.connect()
    cursor = d.cursor()
    query = "DELETE FROM seat WHERE uid = %s AND show_id = %s AND show_time = %s AND status=%s"
    try:
        cursor.execute(query, (userID, showID, showTime, 'Hold'))
        d.commit()
        d.close()
    except Exception as e:
        print(e)
        d.rollback()