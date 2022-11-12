import email
from traceback import print_tb
from models.database import db
from models.encordec.passw import passGen, passCheck
from models.email.userside import *
from models.encordec.cryword import *
import models
import uuid




class userAuth:


    def login(**kwargs):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `userId`,`password`, `active`, `email` FROM `user` WHERE `email` = %s OR `username` = %s", (kwargs['logname'], kwargs['logname']))
        user = cursor.fetchone()

        try:
            l = len(user)
        except:
            l = 0

        if l > 0:
            if passCheck(user[1], kwargs['password']):
                
                if user[2] == 'true':
                    return {"action": "success", "email": user[3], "id": user[0]}
                else:
                    sendActivationEmail(user[3] , wordEnc(user[0]))
                    return {"action": "activation", "email": user[3], "id": user[0]}
            else:
                return False
        else:
            return False

    def register(**kwargs):

        data = {
            "result": False
        }
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO `user`(`firstName`, `lastName`, `email`, `username`, `password`, `PhoneNumber`, `gender`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (kwargs['firstname'], kwargs['lastname'], kwargs['email'], kwargs['username'], passGen(kwargs['password']), kwargs['phonenumber'], kwargs['gender']))
        db.connection.commit()

        #getting user id by email
        id = getEmailId(kwargs['email'])

        #Encryipting user id
        insId = wordEnc(id)

        #send activation link to user
        sendActivationEmail(kwargs['email'] , insId)

        data['result'] = True
        data['data'] = {"userId": insId,"email": kwargs['email']}
        
        return data
    
    def userCheckEmail(email):
        cursor = db.connection.cursor()
        cursor.execute('SELECT `email` FROM `user` WHERE `email` = %s', (email,))
        count = (len(cursor.fetchall()))

        if count >=1:
            return True
        else:
            return False

    def userCheckUsername(username):
        cursor = db.connection.cursor()
        cursor.execute('SELECT `username` FROM `user` WHERE `username` = %s', (username,))
        count = (len(cursor.fetchall()))

        if count >=1:
            return True
        else:
            return False

    def userCheckUsernameItSelf(userid ,username):
        cursor = db.connection.cursor()
        cursor.execute('SELECT `username` FROM `user` WHERE `username` = %s AND `userId` != %s', (username, userid))
        count = (len(cursor.fetchall()))

        if count >=1:
            return True
        else:
            return False
    
    def activateUserById(id):
        cursor = db.connection.cursor()
        cursor.execute("UPDATE `user` SET `active`= 'true' WHERE `userId`= %s", (id,))

        db.connection.commit()
        return True

    def resendActivationLink(userId):

        data = {
            "result": False
        }

        token = wordEnc(userId)
        email = getEmailByUserId(userId)

        if not email:
            return data
        #send activation link to user

        sendActivationEmail(email, token)

        data['result'] = True

        data['data'] = {
            "email": email,
            "userId": token
        }

        return data


    def sendUserTokenResetPassw(email):

        userId = getEmailId(email)
        token = uuid.uuid1()
        exp = models.getExpTime()

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO `passreset`(`userId`, `token`, `exp`) VALUES (%s, %s, %s)", (userId, token, exp))
        db.connection.commit()

        #sending email to reset password
        sendResetPasswEmail(email, wordEnc(userId), token)
        return True
    
    def checkUserExpTokenRP(userId, token):

        cursor = db.connection.cursor()
        cursor.execute("SELECT `exp`,`active`,`passresId` FROM `passreset` WHERE `userId`= %s AND `token`= %s", (userId, token))
        user = cursor.fetchone()
        
        try:
            l = len(user)
        except:
            l = 0
        
        if l > 0:
            if str(user[1]) == 'true':
                updateResetPasswActive(userId, token)
                if models.checkExpTime(str(user[0])):
                    return True
    
    def changeUserPassw(id, passw):
        cursor = db.connection.cursor()
        cursor.execute("UPDATE `user` SET `password`= %s WHERE `userId` = %s", (passGen(passw), id))
        db.connection.commit()
        return True
    
    def ckeckingUserE(id):
        cursor = db.connection.cursor()
        cursor.execute('SELECT `userId` FROM `user` WHERE `userId` = %s AND `userId` != 0;', (id,))
        
        try:
            data = cursor.fetchone()[0]
        except:
            data = False
        
        print('---------------------------------------')
        print(data)
        print('---------------------------------------')
        
        return data
    
def getEmailId(email):
    cursor = db.connection.cursor()
    cursor.execute('SELECT `userId` FROM `user` WHERE `email` = %s', (email,))
    return cursor.fetchone()[0]

def getEmailByUserId(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT `email` FROM `user` WHERE `userId` = %s', (id,))
    
    try:
        data = cursor.fetchone()[0]
    except:
        data = False
    
    return data

def updateResetPasswActive(userId, token):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE `passreset` SET `active`='false' WHERE `userId` = %s AND `token` = %s", (userId,token))
    db.connection.commit()
    return True

