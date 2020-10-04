import server

def feedback(userID, movieName, userName, feedback, rating):
    print('Inside model - feedback', userID, movieName, userName, feedback, rating)
    d = server.mongo
    try:
        doc = {'userID': userID, 'movieName': movieName, 'userName': userName, 'feedback': feedback, 'rating': rating}
        d.db.moviefeedback.insert(doc)
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def getRatingAndFeedback(movieName):
    print('Inside model - getRatingAndFeedback', movieName)
    d = server.mongo
    try:
        cursor = d.db.moviefeedback.find({'movieName': movieName}, {'rating': 1, '_id': 0, 'feedback': 1})
        res = []
        for document in cursor:
            res.append(document)
        return res
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def getAllMovies():
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT DISTINCT mname FROM movie"
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(e)
        return "NOT OK"


def getAllTheaters():
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT tid, tname FROM theater"
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    except Exception as e:
        print (e)
        return "NOT OK"
