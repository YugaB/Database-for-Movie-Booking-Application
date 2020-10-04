import server

def paymentDetails(showID, userID, showTime):
    print('Inside model - paymentDetails', showID, userID, showTime)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT m.mname, sc.show_date, s.seat_id, u.discount, m.price " \
                "FROM movie m JOIN screen sc ON m.mid=sc.mid JOIN seat s ON s.show_id=sc.show_id JOIN user u ON u.uid=s.uid " \
                "WHERE s.uid=%s AND s.show_id=%s AND s.show_time=%s AND s.status=%s"
        cursor.execute(query, (userID, showID, showTime, 'Hold'))
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(e)
        return "NOT OK"