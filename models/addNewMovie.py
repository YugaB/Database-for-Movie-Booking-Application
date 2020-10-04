import server
from datetime import timedelta

def addNewMovie(movieName, genre, price, duration):
    print('Inside model - addNewMovie', movieName, genre, price, duration)
    d = server.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO movie (mname,genre,price,duration) VALUES (%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,
                       (movieName, genre, price, duration))
        d.commit()
        # Commit your changes in the database
        movieID = cursor.lastrowid
        d.close()
        print("inserted", movieName, genre, price, duration)
        return {'statusCode': 200, 'message': 'Movie Inserted Successfully!', 'result': movieID}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def addShowDates(theaterID, movieID, releaseDateObject, endDateObject):
    print('Inside model - addShowDates', theaterID, movieID, releaseDateObject, endDateObject)
    try:
        d = server.mysql.connect()
        d.autocommit_mode = False
        cursor = d.cursor()
        query = "INSERT INTO screen (tid, mid, show_date) VALUES (%s,%s,%s)"

        showDate = releaseDateObject
        while showDate <= endDateObject:
            cursor.execute(query,(theaterID, movieID, showDate))
            print("inserted", theaterID, movieID, showDate)
            showDate = showDate + timedelta(days=1)
        # Commit your changes in the database
        d.commit()
        d.close()
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def unavailableTimeSlots(theaterID, showStartDate, showEndDate):
    print('Inside model - unavailableTimeSlots', theaterID, showStartDate, showEndDate)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT DISTINCT screen.scid, show_time.show_time FROM screen JOIN show_time ON " \
                "screen.show_id=show_time.show_id WHERE tid = %s AND screen.show_date >= %s AND " \
                "screen.show_date <= %s"
        cursor.execute(query, (theaterID, showStartDate, showEndDate))
        results = cursor.fetchall()
        print("result --->", results)
        return results

    except Exception as e:
        print(e)
        return "NOT OK"


def getAllScreenID(theaterID):
    print('Inside model - getAllScreenID', theaterID)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT scid FROM screenSeats WHERE tid = %s"
        cursor.execute(query, theaterID)
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(e)
        return "NOT OK"


def getAllShowID(theaterID, movieID):
    print('Inside model - getAllShowID', theaterID, movieID)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT show_id FROM screen WHERE tid = %s AND mid = %s"
        cursor.execute(query, (theaterID, movieID))
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(e)
        return "NOT OK"


def updateScreenID(screenID, allShowIDList):
    print('Inside model - updateScreenID', screenID, allShowIDList)
    try:
        d = server.mysql.connect()
        d.autocommit_mode = False
        cursor = d.cursor()
        query = "UPDATE screen SET scid = %s WHERE show_id = %s"
        for showID in allShowIDList:
            cursor.execute(query, (screenID, showID))
        d.commit()
        d.close()

    except Exception as e:
        print(e)
        d.rollback()


def addShowTimes(allShowIDList, showTimeObjectList):
    print('Inside model - addShowTimes', allShowIDList, showTimeObjectList)
    try:
        d = server.mysql.connect()
        d.autocommit_mode = False
        cursor = d.cursor()
        query = "INSERT INTO show_time (show_id,show_time) VALUES (%s,%s)"
        # Execute the SQL command
        for showID in allShowIDList:
            for showTime in showTimeObjectList:
                cursor.execute(query, (showID, showTime))
                print("inserted", showID, showTime)
        # Commit your changes in the database
        d.commit()
        d.close()
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def getTheaterID(userID):
    print('Inside model - getTheaterID', userID)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT tid FROM theater WHERE admin_id = %s"
        cursor.execute(query, userID)
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(e)
        return "NOT OK"