import server


def getSeatStatus(showID, showTime):
    print('Inside model - getSeatStatus', showID, showTime)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT show_id, show_time, seat_id FROM seat WHERE show_id = %s AND show_time = %s"
        cursor.execute(query,(showID, showTime))
        results = cursor.fetchall()
        return {'statusCode': 200, 'message': 'Search Successful!', 'result': results}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()



def holdSeats(showID, showTime, allSeats, userID):
    print('Inside model - holdSeats', showID, showTime, allSeats, userID)
    try:
        d = server.mysql.connect()
        d.autocommit_mode = False
        cursor = d.cursor()
        query = "INSERT INTO seat (seat_id,status,show_time,show_id,uid) VALUES (%s,%s,%s,%s,%s)"
        for seatID in allSeats:
            cursor.execute(query, (seatID, 'Hold', showTime, showID, userID))
            print("inserted", seatID, 'Hold', showTime, showID, userID)
        d.commit()
        d.close()
        return {'statusCode': 200, 'message': 'Seat Booking Inserted Successfully!'}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()