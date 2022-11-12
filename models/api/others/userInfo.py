from models.database import db
from models.encordec.passw import passGen, passCheck

class userinfo:

    def allUserDet(userId):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `firstName`, `lastName`, `email`, `username`, `PhoneNumber`, `profile`, `password` FROM `user` WHERE `userId` = %s", (userId,))

        row_headers=[x[0] for x in cursor.description]
        movies = cursor.fetchall()
        json_data=[]

        for result in movies:
            json_data.append(dict(zip(row_headers,result)))

        return json_data
    
    def CheckUserPassw(userId, passw):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `password` FROM `user` WHERE `userId` = %s", (userId,))
        user = cursor.fetchone()

        if passCheck(user[0], passw):
            return True
        else:
            return False

    def updateuserInfo(userId, **kwargs):
        cursor = db.connection.cursor()
        try:
            cursor.execute("UPDATE `user` SET `firstName`= %s,`lastName`= %s,`username` = %s ,`PhoneNumber`=  %s,`profile`= %s WHERE `userId` = %s", (kwargs["firstName"], kwargs["lastName"],kwargs["username"], kwargs["PhoneNumber"], kwargs["profile"], userId))
            db.connection.commit()
        except:
            return False

        return True
    
    