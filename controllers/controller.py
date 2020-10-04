from datetime import datetime

import models.signIn
import models.signUp
import models.addNewMovie
import models.movieFeedback
import models.theaterFeedback
import models.addNewTheater
import models.movieSearch
import models.delete_seat_status
import models.seatBooking
import models.applyDiscount
import models.payment
import models.change_seat_status


def signin(name, email, password, role):
    res = models.signIn.login(name, email, password, role)
    if role == 'Admin' and res['statusCode'] == 200:
        adminID = res['result'][0][0]
        theaterID = models.addNewMovie.getTheaterID(adminID)
        print('theaterID: ', theaterID[0][0])
        finalRes = {'theaterID': theaterID[0][0], 'res': res['result']}
        return {"statusCode": 200, "message": "Success", "result": finalRes}
    elif role == 'User' and res['statusCode'] == 200:
        finalRes = {'res': res['result']}
        return {"statusCode": 200, "message": "Success", "result": finalRes}
    else:
        return res


def signup(name, email, password, role):
    return models.signUp.signup(name, email, password, role)


def addNewTheater(theaterName, address, state, city, phone, adminID, screenID):
    theaterID = models.addNewTheater.addNewTheater(theaterName, address, state, city, phone, adminID)
    models.addNewTheater.addScreens(theaterID, screenID)
    return {'statusCode': 200, 'message': 'Theater Inserted Successfully!', 'result': theaterID}


def addNewMovie(movieName, genre, price, duration, firstDateObject, lastDateObject, theaterID):
    res = models.addNewMovie.addNewMovie(movieName, genre, price, duration)
    if res['statusCode'] == 200:
        movieID = res['result']
        addShowsDates(int(theaterID), int(movieID), firstDateObject, lastDateObject)
        bookedSlots = models.addNewMovie.unavailableTimeSlots(theaterID,firstDateObject, lastDateObject)
        bookedSlotsDict = {}
        for slot in bookedSlots:
            if slot[0] not in bookedSlotsDict:
                bookedSlotsDict[slot[0]] = []
            bookedSlotsDict[slot[0]].append(str(slot[1]))

        allScreenID = models.addNewMovie.getAllScreenID(theaterID)
        allScreenIDList = []
        for screenID in allScreenID:
            allScreenIDList.append(screenID[0])

        finalRes = {'bookedSlots': bookedSlotsDict, 'allScreenID': allScreenIDList, 'theaterID': theaterID, 'movieID': movieID}
        return {'statusCode': 200, 'message': 'Successfully!', 'result': finalRes}


def addShowsDates(theaterID, movieID, releaseDateObject, endDateObject):
    models.addNewMovie.addShowDates(theaterID, movieID, releaseDateObject, endDateObject)
    print("Successfully inserted!")


def addShowTimes(screenID, showTimeObjectList, theaterID, movieID):
    allShowID = models.addNewMovie.getAllShowID(theaterID, movieID)
    allShowIDList = []
    for showID in allShowID:
        allShowIDList.append(showID[0])

    models.addNewMovie.updateScreenID(screenID, allShowIDList)

    models.addNewMovie.addShowTimes(allShowIDList, showTimeObjectList)


def initialMovieSearch(city, showDate):
    showDateObj = (datetime.strptime(showDate, '%Y-%m-%d'))
    res = models.movieSearch.initialSearch(city, showDateObj)
    allMovieDetails = {}
    for entry in res['result']:
        if entry[7] in allMovieDetails:
            tempDict = {}
            tempDict['movieID'] = entry[2]
            tempDict['movieName'] = entry[0]
            tempDict['genre'] = entry[1]
            allMovieDetails[entry[7]]['movies'].append(tempDict)
        else:
            allMovieDetails[entry[7]] = {}
            allMovieDetails[entry[7]]['theaterName'] = entry[3]
            allMovieDetails[entry[7]]['address'] = entry[4] + ',' + entry[5] + ',' + entry[6]
            allMovieDetails[entry[7]]['movies'] = []
            tempDict = {}
            tempDict['movieID'] = entry[2]
            tempDict['movieName'] = entry[0]
            tempDict['genre'] = entry[1]
            allMovieDetails[entry[7]]['movies'].append(tempDict)

    allTheaterFeedbacks = {}
    for theaterID in allMovieDetails:
        t = getTheaterratingAndFeedback(theaterID)
        if theaterID not in allTheaterFeedbacks and t[0] != 0.0:
            allTheaterFeedbacks[theaterID] = t
    print("allTheaterFeedbacks --->", allTheaterFeedbacks)

    allMovieFeedbacks = {}
    for theaterID in allMovieDetails:
        for movie in allMovieDetails[theaterID]['movies']:
            movieName = movie['movieName']
            m = getMovieRatingAndFeedback(movieName)
            if movieName not in allMovieFeedbacks and m[0] != 0.0:
                allMovieFeedbacks[movieName] = m
    print("allMovieFeedbacks ---->", allMovieFeedbacks)

    return {'allMovieDetails': allMovieDetails, 'allTheaterFeedbacks': allTheaterFeedbacks, 'allMovieFeedbacks': allMovieFeedbacks}


def filter(city, showDate, theaterName, movieName, genre):
    res = models.movieSearch.filter(city, showDate, theaterName, movieName, genre)
    allMovieDetails = {}
    for entry in res['result']:
        if entry[7] in allMovieDetails:
            tempDict = {}
            tempDict['movieID'] = entry[2]
            tempDict['movieName'] = entry[0]
            tempDict['genre'] = entry[1]
            allMovieDetails[entry[7]]['movies'].append(tempDict)
        else:
            allMovieDetails[entry[7]] = {}
            allMovieDetails[entry[7]]['theaterName'] = entry[3]
            allMovieDetails[entry[7]]['address'] = entry[4] + ',' + entry[5] + ',' + entry[6]
            allMovieDetails[entry[7]]['movies'] = []
            tempDict = {}
            tempDict['movieID'] = entry[2]
            tempDict['movieName'] = entry[0]
            tempDict['genre'] = entry[1]
            allMovieDetails[entry[7]]['movies'].append(tempDict)

    allTheaterFeedbacks = {}
    for theaterID in allMovieDetails:
        t = getTheaterratingAndFeedback(theaterID)
        if theaterID not in allTheaterFeedbacks and t[0] != 0.0:
            allTheaterFeedbacks[theaterID] = t

    allMovieFeedbacks = {}
    for theaterID in allMovieDetails:
        for movie in allMovieDetails[theaterID]['movies']:
            movieName = movie['movieName']
            m = getMovieRatingAndFeedback(movieName)
            if movieName not in allMovieFeedbacks and m[0] != 0.0:
                allMovieFeedbacks[movieName] = m

    return {'allMovieDetails': allMovieDetails, 'allTheaterFeedbacks': allTheaterFeedbacks, 'allMovieFeedbacks': allMovieFeedbacks}


def getShowTimes(theaterID, movieID, showDate):
    data = models.movieSearch.getShowTimes(theaterID, movieID, showDate)
    showList = []
    showID = data['result'][0][0]
    for entry in data['result']:
        showList.append(str(entry[1]))
    return showID, showList


def getSeatStatus(showID, showTime):
    res = models.seatBooking.getSeatStatus(showID, showTime)
    allReservedSeats = []
    for reservation in res['result']:
        allReservedSeats.append(reservation[2])
    return allReservedSeats


def holdSeats(showID, showTime, seatInfo, userID):
    allSeats = []
    for seat in seatInfo:
        seatList = seat.split('-')
        seat_row = chr(int(seatList[0]) + 64)
        seat_col = seatList[1]
        s = seat_row + '' + seat_col
        allSeats.append(s)
    models.seatBooking.holdSeats(showID, showTime, allSeats, userID)


def checkForDiscount(userID):
    models.applyDiscount.checkDiscount(userID)


def paymentDetails(showID, userID, showTime):
    res = models.payment.paymentDetails(showID, userID, showTime)
    seatList = []
    movieName = res[0][0]
    showDate = res[0][1]
    discount = res[0][3]
    price = res[0][4]
    for entry in res:
        seatList.append(entry[2])
    return {'movieName': movieName, 'showDate': showDate, 'discount': discount, 'seatList': seatList, 'price': price}


def updateSeatStatus(userID, showID, showTime):
    models.change_seat_status.changeSeatStatus(userID, showID, showTime)


def deleteSeat(userID, showID, showTime):
    models.delete_seat_status.deleteSeattatus(userID, showID, showTime)


def getAllMovies():
    allMovies = models.movieFeedback.getAllMovies()
    allMoviesList = []
    for entry in allMovies:
        allMoviesList.append(entry[0])
    return allMoviesList


def movieFeedback(userID, movieName, userName, feedback, rating):
    models.movieFeedback.feedback(userID, movieName, userName, feedback, rating)


def getMovieRatingAndFeedback(movieName):
    documentsList = models.movieFeedback.getRatingAndFeedback(movieName)
    allFeedbacks = []
    total = 0.0
    count = 0
    finalRating = 0.0
    if len(documentsList) != 0:
        for document in documentsList:
            count += 1
            total += float(document['rating'])
            allFeedbacks.append(document['feedback'])
        finalRating = float(total) / count
    return round(finalRating, 2), allFeedbacks


def getAllTheaters():
    allTheaters = models.movieFeedback.getAllTheaters()
    allTheatersDict = {}
    for entry in allTheaters:
        allTheatersDict[entry[0]] = entry[1]
    return allTheatersDict


def theaterFeedback(userID, theaterID, userName, feedback, rating):
    return models.theaterFeedback.feedback(userID, theaterID, userName, feedback, rating)


def getTheaterratingAndFeedback(theaterID):
    documentsList = models.theaterFeedback.getRatingAndFeedback(theaterID)
    allFeedbacks = []
    total = 0.0
    count = 0
    finalRating = 0.0
    if len(documentsList) != 0:
        for document in documentsList:
            count += 1
            total += float(document['rating'])
            allFeedbacks.append(document['feedback'])
        finalRating = float(total) / count
    return round(finalRating, 2), allFeedbacks

