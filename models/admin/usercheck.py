import re
from werkzeug.security import generate_password_hash
from models.database import db

class usercheck:
    def __init__(self, firstname, lastname, email, username, phonenumber, gender, passw, cpassw):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.phonenumber = phonenumber
        self.gender = gender
        self.passw = passw
        self.cpassw = cpassw
        self.mysql = db
        self.regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.regPass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    
    def passwordValidate(self):

        if self.passw == self.cpassw:   
            mat = re.search(re.compile(self.regPass), self.passw)
            if mat:
                return True
            else:
                return False
        else:
            return False
    
    def EmailValidate(self):
        if(re.search(self.regexEmail, self.email)):   
            return True 
        else:   
            return False 
    
    def checkEmailUnique(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `adminuser` WHERE `email`= %s", (self.email,))
        count = (len(cur.fetchall()))

        if count >=1:
            return False
        else:
            return True

    def checkUsernameUnique(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `adminuser` WHERE `username` = %s", (self.username,))
        count = (len(cur.fetchall()))

        if count >=1:
            return False
        else:
            return True
    
    def getD(self):
        if self.checkUsernameUnique() and self.checkEmailUnique() and self.EmailValidate() and self.passwordValidate():
            return True
        else:
            return False
    
    def insertUser(self):
        if self.getD():
            passw = generate_password_hash(self.passw)
            cur = self.mysql.connection.cursor()
            cur.execute("INSERT INTO `adminuser`(`firstname`, `lastname`, `email`, `username`, `phonenumber`, `password`, `gender`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.firstname, self.lastname, self.email, self.username, self.phonenumber, passw, self.gender))
            self.mysql.connection.commit()
            return True
        else:
            return False


class getUserId:
    def __init__(self, email):
        self.mysql = db
        self.email = email
    
    def getuser(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `adminuser` WHERE `email`= %s", (self.email,))
        user = cur.fetchall()

        if len(user) == 1:
            return user[0]
        else:
            return False
        
    def disableV(self):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE `adminuser` SET `verified`='false' WHERE `email`= %s", (self.email,))
        self.mysql.connection.commit()


class setNewPassw:
    def __init__(self, passw, id):
        self.mysql = db
        self.passw = passw
        self.id = id
    
    def setnewpass(self):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE `adminuser` SET `password`=%s WHERE `AdminId` = %s", (self.passw, self.id))
        self.mysql.connection.commit()

        return True

class getUserInfo:
    def __init__(self, id):
        self.mysql = db
        self.id = id
    
    def getuser(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `adminuser` WHERE `AdminId`= %s", (self.id,))
        user = cur.fetchone()
        return user

class updateUserInfo:
    def __init__(self, userId, firstname, lastname, phoneNumber, image):
        self.mysql = db
        self.userId = userId
        self.firstname = firstname
        self.lastname = lastname
        self.phoneNumber = phoneNumber
        self.image = image

    def update(self):
        
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE `adminuser` SET `firstname`= %s,`lastname`= %s,`phonenumber`= %s,`profile`=%s WHERE `AdminId` = %s", (self.firstname,self.lastname, self.phoneNumber, self.image, self.userId))
        self.mysql.connection.commit()