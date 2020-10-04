import server

def feedback(userID, theaterID, userName, feedback, rating):
    print('Inside model - feedback', userID, theaterID, userName, feedback, rating)
    d = server.mongo
    try:
        doc = {'userID': userID, 'theaterID': theaterID, 'userName': userName, 'feedback': feedback, 'rating': rating}
        d.db.theaterfeedback.insert(doc)
        return {'status': 'Inserted'}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def getRatingAndFeedback(theaterID):
    print('Inside model - getRatingAndFeedback', theaterID)
    d = server.mongo
    try:
        cursor = d.db.theaterfeedback.find({'theaterID': theaterID}, {'rating': 1, '_id': 0, 'feedback': 1})
        res = []
        for document in cursor:
            res.append(document)
        return res
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()
