import server

def changeSeatStatus(userID, showID, showTime):
    print('Inside model - changeSeatStatus', userID, showID, showTime)
    d = server.mysql.connect()
    cursor = d.cursor()
    query = "UPDATE seat SET status=%s WHERE uid = %s AND show_id = %s AND show_time = %s"
    try:
        cursor.execute(query, ('Booked', userID, showID, showTime))
        d.commit()
        d.close()
    except Exception as e:
        print(e)
        d.rollback()