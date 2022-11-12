import re   
import random
from models.database import db
from flask import session


def Emailcheck(email):   
  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

    if(re.search(regex, email)):   
        return True 
    else:   
        return False 
    
def verifyUser(userid):
    cur = db.connection.cursor()
    cur.execute("UPDATE `adminuser` SET `verified`='true' WHERE `AdminId`= %s", (userid,))
    
    db.connection.commit()

def verifyUserCode(id):
    cur = db.connection.cursor()
    cur.execute("UPDATE `admincode` SET `visible`='false' WHERE `codeId`= %s", (id,))
    
    db.connection.commit()

def sendCodeUser(userid, code):
    cur = db.connection.cursor()
    cur.execute("INSERT INTO `admincode`(`adminId`, `code`) VALUES (%s, %s)", (userid, code))
    
    db.connection.commit()

def gencode():
    n = []
    code = ''
    for i in range(1, 101):
        n.append(i)
    for _ in range(5):
        code += str(random.choice(n))
    
    return code

def setSession(id):
    session['userId'] = id

def checkSession():
    if 'userId' in session:
        return True
    else:
        return False

def checkcodeUserEnt(userid, codeG):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM `admincode` WHERE `adminId`=%s AND `visible`= 'true'", (userid,))
    ''' code = cur.fetchone()
    if code[2] == codeG:
        verifyUser(userid)
        verifyUserCode(code[0])
        return True
    else:
        return False '''

    code = cur.fetchall()

    for i in code:
        if i[2] == codeG:
            verifyUser(userid)
            verifyUserCode(i[0])
            return True
    
    return False

def genreAll():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM `genre` WHERE `visible`='true' ORDER BY `genreId` DESC")

    return cur.fetchall()