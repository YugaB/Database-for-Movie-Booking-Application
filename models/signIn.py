import server
import bcrypt

def login(name, email, password, role):
    print('Inside model - login', name, email, password, role)
    try:
        d = server.mysql.connect()
        cursor = d.cursor()
        query = "SELECT uid, name, email, password, role FROM user WHERE email = %s AND role = %s"
        cursor.execute(query, (email, role))
        results = cursor.fetchall()
        print("result --->", results)
        if not results:
            return {"statusCode": 400, "message": "Invalid Email"}
        else:
            matchRes = bcrypt.checkpw(password.encode('utf8'), results[0][3].encode('utf8'))
            if matchRes == False:
                return {"statusCode": 400, "message": "Invalid Password"}
        return {"statusCode": 200, "message": "Success", "result": results}

    except Exception as e:
        print(e)
        return "NOT OK"