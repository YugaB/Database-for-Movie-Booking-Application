from flask import Flask, session
from flask import request, render_template
from flaskext.mysql import MySQL
from flask import jsonify
from datetime import datetime

import controllers.controller
from flask_pymongo import PyMongo

app = Flask(__name__)
app.logger.disabled = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL()
app.config["MONGO_URI"] = "mongodb://nrupa:16Jan91*@ds149742.mlab.com:49742/cmpe226"
mongo = PyMongo(app)
app.config['MYSQL_DATABASE_USER'] = 'nrupa'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cmpe226'
app.config['MYSQL_DATABASE_DB'] = 'cmpe226'
app.config['MYSQL_DATABASE_HOST'] = 'cmpe226.csdalav6vzak.us-west-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@app.errorhandler(400)
def bad_request(s, error=None):
    message = {
        'status': 400,
        'message': 'BAD REQUEST ' + request.url,
        'reason': error,
        'parameter': s,
    }
    print ("Error Message: ", message)
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.route("/")
def landing():
    return render_template('landing.html')


@app.route("/adminSignIn")
def adminSignIn():
    return render_template('adminSignIn.html')


@app.route("/userSignIn")
def userSignIn():
    return render_template('userSignIn.html')


@app.route("/adminSignUp")
def adminSignUp():
    return render_template('adminSignUp.html')


@app.route("/userLogout")
def userLogout():
    return render_template('signOut.html')


@app.route("/userSignUp")
def userSignUp():
    return render_template('userSignUp.html')


@app.route("/signin", methods=["GET", "POST"])
def signin():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    if len(name) == 0:
        return bad_request(name)

    if len(password) == 0:
        return bad_request(password)

    if len(email) == 0:
        return bad_request(email)

    res = controllers.controller.signin(name, email, password, role)
    print('res---> ', res)
    if res['statusCode'] == 400:
        if role == "Admin":
            return render_template('adminSignIn.html', error=res['message'])
        else:
            return render_template('userSignIn.html', error=res['message'])
    else:
        userID = res['result']['res'][0][0]
        userName = res['result']['res'][0][1]
        session['logged_in'] = {'userID': userID, 'userName': name}
        if role == 'Admin':
            return render_template('addMovie.html', theaterID=res['result']['theaterID'])
        else:
            controllers.controller.checkForDiscount(userID)
            return render_template('landing.html', userName=userName)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    if len(name) == 0:
        return bad_request(name)

    if len(password) == 0:
        return bad_request(password)

    if len(email) == 0:
        return bad_request(email)

    res = controllers.controller.signup(name, email, password, role)
    session['logged_in'] = {'userID': res['result'], 'userName': name}
    if role == "Admin":
        return render_template('addTheater.html', adminID=res['result'])
    else:
        return render_template('landing.html', userName=name)


@app.route("/addtheater", methods=["GET", "POST"])
def addNewTheater():
    theaterName = request.form['theaterName']
    address = request.form['address']
    state = request.form['state']
    city = request.form['city']
    phone = request.form['phone']
    screenID = request.form['screenID']
    adminID = int(request.form['adminID'])

    if len(theaterName) == 0:
        return bad_request(theaterName)

    if len(address) == 0:
        return bad_request(address)

    if len(state) == 0:
        return bad_request(state)

    if len(city) == 0:
        return bad_request(city)

    if len(phone) == 0:
        return bad_request(phone)

    if len(screenID) == 0:
        return bad_request(screenID)

    res = controllers.controller.addNewTheater(theaterName, address, state, city, phone, adminID, screenID)
    if res['statusCode'] == 200:
        return render_template('addMovie.html', theaterID=res['result'])


@app.route("/addmovie", methods=["GET", "POST"])
def addNewMovie():
    movieName = request.form['movieName']
    genre = request.form['genre']
    price = float(request.form['price'])
    duration = int(request.form['duration'])
    firstDate = request.form['firstDate']
    lastDate = request.form['lastDate']
    theaterID = int(request.form['theaterID'])

    if len(movieName) == 0:
        return bad_request(movieName)

    if len(genre) == 0:
        return bad_request(genre)

    if price <= 0:
        return bad_request(price)

    if duration <= 0:
        return bad_request(duration)

    try:
        firstDateObject = (datetime.strptime(firstDate, '%Y-%m-%d'))
    except ValueError:
        return bad_request(firstDate)
    try:
        lastDateObject = (datetime.strptime(lastDate, '%Y-%m-%d'))
    except ValueError:
        return bad_request(lastDate)

    res = controllers.controller.addNewMovie(movieName, genre, price, duration, firstDateObject, lastDateObject, theaterID)
    print('res ---->', res)
    return render_template('addMovieShowTimes.html', bookedSlots=res['result']['bookedSlots'], allScreenID=res['result']['allScreenID'], totalScreens=len(res['result']['allScreenID']), theaterID=res['result']['theaterID'], movieID=res['result']['movieID'])


@app.route("/addShows", methods=["POST"])
def addShowTimes():
    screenID = request.form['screenID']
    showTime = request.form['showTime']
    theaterID = int(request.form['theaterID'])
    movieID = int(request.form['movieID'])

    if len(screenID) == 0:
        return bad_request(screenID)

    showTimeList = showTime.split(',')
    showTimeObjectList = []

    try:
        for time in showTimeList:
            timeObject = (datetime.strptime(time, '%H:%M:%S'))
            showTimeObjectList.append(timeObject)
    except ValueError:
        return bad_request(time)

    res = controllers.controller.addShowTimes(screenID, showTimeObjectList, theaterID, movieID)
    return render_template('signOut.html')


@app.route("/initialMovieTheaterSearch", methods=["POST"])
def initialMovieTheaterSearch():
    city = request.form['city']
    date = request.form['date']
    res = controllers.controller.initialMovieSearch(city, date)
    return render_template('displayMovies.html', allMovies=res['allMovieDetails'], allTheaterFeedbacks=res['allTheaterFeedbacks'], allMovieFeedbacks=res['allMovieFeedbacks'], showdate=date, city=city)


@app.route("/filter", methods=["GET", "POST"])
def filter():
    movieName = request.form['movie']
    theaterName = request.form['theater']
    genre = request.form['genre']
    showDate = request.form['showDate']
    city = request.form['city']
    res = controllers.controller.filter(city, showDate, theaterName, movieName, genre)
    return render_template('displayMovies.html', allMovies=res['allMovieDetails'], allTheaterFeedbacks=res['allTheaterFeedbacks'], allMovieFeedbacks=res['allMovieFeedbacks'], showdate=showDate, city=city)


@app.route("/movieShowTimes", methods=["GET", "POST"])
def movieShowTimes():
    theaterObj = request.form['theaterObj']
    theaterList = theaterObj.split('/')
    theaterID = theaterList[0]
    theaterName = theaterList[1]
    movieObj = request.form['movieObj']
    movieList = movieObj.split('/')
    movieID = movieList[0]
    movieName = movieList[1]
    showDate = request.form['showDate']
    res1, res2 = controllers.controller.getShowTimes(theaterID, movieID, showDate)
    return render_template('showTimeDisplay.html', showID=res1, showTimes=res2, theaterName=theaterName, movieName=movieName)


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if session:
        showTime = request.form['showTime']
        showID = request.form['showID']
        print('showTime ---->', showTime, 'showID --->', showID)
        res = controllers.controller.getSeatStatus(showID, showTime)
        print ('res -->', res)
        if not res or len(res) == 0:
            return render_template('seatBooking.html', showTime=showTime, showID=showID)
        else:
            d = {65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E'}
            return render_template('updateSeatBooking.html', showTime=showTime, showID=showID, bookedSeats=res, mapping=d)
    else:
        return render_template('userSignIn.html')


@app.route("/holdSeats", methods=["GET", "POST"])
def holdSeats():
    showID = request.form['showID']
    showTime = request.form['showTime']
    seatInfo = request.form.getlist('seatInfo')
    userID = session['logged_in']['userID']
    timeObject = datetime.strptime(showTime, '%H:%M:%S')
    print(showID, showTime, seatInfo)
    controllers.controller.holdSeats(showID, timeObject, seatInfo, userID)
    res = controllers.controller.paymentDetails(showID, userID, showTime)
    return render_template('payment.html', movieName=res['movieName'], showTime=showTime, showDate=res['showDate'], discount=res['discount'], showID=showID, userID=userID, seatInfo=res['seatList'], price=res['price'])


@app.route("/payment", methods=["GET", "POST"])
def payment():
    userID = request.form['userID']
    showID = request.form['showID']
    showTime = request.form['showTime']
    decision = request.form['decision']
    print(userID, showID, showTime, decision)
    if decision == 'Yes':
        controllers.controller.updateSeatStatus(userID, showID, showTime)
        return render_template('signOut.html')
    else:
        controllers.controller.deleteSeat(userID, showID, showTime)
        return render_template('signOut.html')


@app.route("/movieFeedback", methods=["GET"])
def movieFeedback():
    res = controllers.controller.getAllMovies()
    return render_template('movieFeedback.html', allMovies=res)


@app.route("/theaterFeedback", methods=["GET"])
def theaterFeedback():
    res = controllers.controller.getAllTheaters()
    return render_template('theaterFeedback.html', allTheaters=res)


@app.route("/addFeedbackMovie", methods=["POST"])
def addFeedbackMovie():
    userID = session['logged_in']['userID']
    userName = session['logged_in']['userName']
    movieName = request.form['movieName']
    feedback = request.form['feedback']
    rating = float(request.form['rating'])

    controllers.controller.movieFeedback(userID, movieName, userName, feedback, rating)
    return render_template('landing.html', userName=userName)


@app.route("/getMovieRatingAndFeedback", methods=["GET"])
def getMovieRatingAndFeedback():
    movieName = request.form['movieName']
    res = controllers.controller.getMovieRatingAndFeedback(movieName)
    return jsonify(res)


@app.route("/addFeedbackTheater", methods=["POST"])
def addFeedbackTheater():
    userID = session['logged_in']['userID']
    userName = session['logged_in']['userName']
    theaterID = int(request.form['theaterID'])
    feedback = request.form['feedback']
    rating = float(request.form['rating'])

    res = controllers.controller.theaterFeedback(userID, theaterID, userName, feedback, rating)
    return render_template('landing.html', userName=userName)


@app.route("/getTheaterRatingAndFeedback", methods=["GET"])
def getTheaterRatingAndFeedback():
    theaterID = int(request.form['theaterID'])
    res = controllers.controller.getTheaterratingAndFeedback(theaterID)
    return jsonify(res)


@app.route("/confirmBooking", methods=["POST"])
def confirm_booking():
    decision = request.form['decision']
    complete_info_list = request.form['complete_info_list']

    if decision == "Yes":
        controllers.control.confirm_booking(complete_info_list)
        message = 'Booking Confirmed'
        return jsonify(message)
    else:
        controllers.control.delete_booking(complete_info_list)
        message = 'Booking Cancelled'
        return jsonify(message)



@app.route('/logout', methods=["POST"])
def logout():
    session.pop('logged_in')
    return render_template('landing.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
