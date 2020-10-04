import server

def addNewTheater(theaterName, address, state, city, phone, adminID):
    print('Inside model - addNewTheater', theaterName, address, state, city, phone, adminID)
    d = server.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO theater (tname,address,state,city,phone,admin_id) VALUES (%s,%s,%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,
                       (theaterName, address, state, city, phone, adminID))
        d.commit()
        # Commit your changes in the database
        theaterID = cursor.lastrowid
        d.close()
        print("inserted", theaterName, address, state, city, phone, adminID)
        return theaterID
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def addScreens(theaterID, allScreenIDs):
    print('Inside model - addScreens', theaterID, allScreenIDs)
    screenIDList = allScreenIDs.split(',')
    try:
        d = server.mysql.connect()
        d.autocommit_mode = False
        cursor = d.cursor()
        query = "INSERT INTO screenSeats (tid,scid,total_seats) VALUES (%s,%s,%s)"
        for scID in screenIDList:
            cursor.execute(query,(theaterID, scID, 50))
            print("inserted", theaterID, scID)
        d.commit()
        d.close()
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()