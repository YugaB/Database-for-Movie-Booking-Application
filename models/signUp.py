import server
import bcrypt

def signup(name, email, password, role):
    print('Inside model - signup', name, email, password, role)
    encryptpassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))
    d = server.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO user (name, email, password, role) VALUES (%s,%s, %s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query, (name, email, encryptpassword, role))
        d.commit()
        userID = cursor.lastrowid
        d.close()
        # Commit your changes in the database
        print("inserted", name, email)
        return {"statusCode": 200, "message": "Success", "result": userID}
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()
