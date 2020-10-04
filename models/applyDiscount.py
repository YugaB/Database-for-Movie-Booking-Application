import server
from datetime import datetime

def checkDiscount(userID):
    print('Inside model - checkDiscount', userID)
    festDates=["2019-05-02"]
    todayDate=datetime.today().strftime('%Y-%m-%d')
    print("today date", todayDate,type(todayDate))
    try:
        d = server.mysql.connect()
        d.autocommit_mode = False
        cursor = d.cursor()
        q1 = "SELECT count(uid) FROM seat WHERE uid = %s"
        cursor.execute(q1, (userID))
        r1=cursor.fetchone()
        print("user count --->", r1[0])
        discount = 0
        userMovieCount = r1[0]
        if userMovieCount >= 10 and userMovieCount <= 15:
            discount = 10
        elif userMovieCount >= 15:
            discount = 15
        elif todayDate in festDates:
            discount = 5
        print("discount", discount)

        q2 = "UPDATE user SET discount=%s where uid=%s"
        cursor.execute(q2, (discount, userID))
        d.commit()
        d.close()
        return {"statusCode": 200, "message": "Success"}

    except Exception as e:
        print(e)
        d.rollback()