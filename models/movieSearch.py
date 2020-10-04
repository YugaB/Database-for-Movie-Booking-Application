import server

def initialSearch(city, showDate):
    print('Inside model - initialSearch', city, showDate)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT * FROM initialMovieSearch WHERE city = %s AND show_date = %s"
        cursor.execute(query,(city, showDate))
        results = cursor.fetchall()
        return {'statusCode': 200, 'message': 'Search Successful!', 'result': results}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def getShowTimes(theaterID, movieID, showDate):
    print('Inside model - getShowTimes', theaterID, movieID, showDate)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        cursor.callproc('show_times_sp',(theaterID, movieID, showDate, 0, 0))
        results = cursor.fetchall()
        return {'statusCode': 200, 'message': 'Got Show Times Successfully!', 'result': results}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def filter(city, showDate, theaterName, movieName, genre):
    print('Inside model - filter', city, showDate, theaterName, movieName, genre)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        cursor.callproc('Get_movie_detail_sp',(city, showDate, movieName, theaterName, genre))
        results = cursor.fetchall()
        return {'statusCode': 200, 'message': 'Got Filter Results Successfully!', 'result': results}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()