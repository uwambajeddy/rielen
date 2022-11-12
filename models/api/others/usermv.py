from cgi import print_arguments
from enum import Flag
from sqlite3 import Cursor
from models.database import db
from models.email.userside import *
from models.encordec.cryword import *
import models
import uuid
import json

from models.exptime import checkExpTime, checkUserNotExpTime, getUserNotExpTime
from routes.api.usermv import userNotif

class userFetch:

    def homeslides():
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`, `movie`.`coverImage`, `movie`.`Description`, `homeslide`.`btnVisible`, `homeslide`.`type` FROM `homeslide` JOIN `movie` ON `homeslide`.`movieId` = `movie`.`movieId` WHERE `homeslide`.`visibility` = 'true' AND `movie`.`visibility` = 'true' ORDER BY `homeslide`.`hmId` DESC")

        return list(cursor.fetchall())

    def allMovies():
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movieId`, `movieTitle`, `otherImage`, `smallTitle`,`trailer`,`writter`,`Description`,`cast`,`coverImage`,`director`,`otherImage` FROM `movie` WHERE `visibility` = 'true' ORDER BY `movieId` DESC")

        movies = list(cursor.fetchall())

        for i in movies:
            i["genres"] = getGenreByMvId(i["movieId"])

        return movies

    def allMoviesByUser(userId):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movieId`, `movieTitle`, `otherImage`, `smallTitle`,`trailer`,`writter`,`Description`,`cast`,`coverImage`,`director`, `otherImage`, (SELECT `visible` FROM `mylist` WHERE `mylist`.`userId` = %s AND `mylist`.`movieId` = mv.`movieId` AND `mylist`.`visible` = 'true') AS mylist FROM `movie` AS mv WHERE mv.`visibility` = 'true' ORDER BY  mv.`movieId` DESC", (userId,))

        movies = list(cursor.fetchall())

        for i in movies:
            i["genres"] = getGenreByMvId(i["movieId"])

            if i['mylist'] == 'true':
                i["mylist"] = True
            else:
                i["mylist"] = False

        return movies

    def singleMovie(id):
        cursor = db.connection.cursor()

        cursor.execute("SELECT `movieId`, `movieTitle`, `otherImage`, `smallTitle`,`trailer`,`writter`,`Description`,`cast`,`coverImage`,`director`, `otherImage` FROM `movie` WHERE `movieId` = %s AND `visibility` = 'true'", (id,))

        movies = list(cursor.fetchall())
            
        if len(movies) != 0:
            movies[0]['gernes'] = getGenreByMvId(id)
        
        return movies

    def getGenres():
        cursor = db.connection.cursor()
        cursor.execute("SELECT `genreId`, `name` FROM `genre` WHERE `visible` = 'true'")
        return list(cursor.fetchall())

    def getGenre(name):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `genreId`, `name` FROM `genre` WHERE `name` = %s AND `visible` = 'true'", (name,))

        return list(cursor.fetchall())

    def moviesByGenre(name, sort):
        cursor = db.connection.cursor()

        if sort == 'DESC':
            cursor.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`,`movie`.`smallTitle`,`movie`.`Description`,`movie`.`cast`,`movie`.`director`,`movie`.`time`,`movie`.`age`,`movie`.`trailer`,`movie`.`writter`,`movie`.`coverImage`,`movie`.`otherImage` FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` ON `genrem`.`movieId` = `movie`.`movieId` WHERE `genre`.`name` = %s AND `movie`.`visibility` = 'true' ORDER BY `movie`.`movieId` DESC", (name,))
        else:
            cursor.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`,`movie`.`smallTitle`,`movie`.`Description`,`movie`.`cast`,`movie`.`director`,`movie`.`time`,`movie`.`age`,`movie`.`trailer`,`movie`.`writter`,`movie`.`coverImage`,`movie`.`otherImage` FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` ON `genrem`.`movieId` = `movie`.`movieId` WHERE `genre`.`name` = %s AND `movie`.`visibility` = 'true' ORDER BY `movie`.`movieId` ASC", (name,))
            
        return list(cursor.fetchall())

    def moviesByGenreByUser(userId, name, sort):
        cursor = db.connection.cursor()

        if sort == 'DESC':
            cursor.execute("SELECT mv.`movieId`,mv.`movieTitle`,mv.`smallTitle`,mv.`Description`,mv.`cast`,mv.`director`,mv.`time`,mv.`age`,mv.`trailer`,mv.`writter`,mv.`coverImage`,mv.`otherImage`, (SELECT `visible` FROM `mylist` WHERE `mylist`.`userId` = %s AND `mylist`.`movieId` = mv.`movieId` AND `mylist`.`visible` = 'true') AS mylist FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` AS mv ON `genrem`.`movieId` = mv.`movieId` WHERE `genre`.`name` = %s AND mv.`visibility` = 'true' ORDER BY mv.`movieId` DESC", (userId, name))
        else:
            cursor.execute("SELECT mv.`movieId`,mv.`movieTitle`,mv.`smallTitle`,mv.`Description`,mv.`cast`,mv.`director`,mv.`time`,mv.`age`,mv.`trailer`,mv.`writter`,mv.`coverImage`,mv.`otherImage`, (SELECT `visible` FROM `mylist` WHERE `mylist`.`userId` = %s AND `mylist`.`movieId` = mv.`movieId` AND `mylist`.`visible` = 'true') AS mylist FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` AS mv ON `genrem`.`movieId` = mv.`movieId` WHERE `genre`.`name` = %s AND mv.`visibility` = 'true' ORDER BY mv.`movieId` ASC", (userId, name))
            
        movies = list(cursor.fetchall())
        
        for i in movies:
    
            if i['mylist'] == 'true':
                i["mylist"] = True
            else:
                i["mylist"] = False
                
        return movies

    def search(search):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movieId`, `movieTitle`, `otherImage`, `smallTitle`,`trailer`,`writter`,`Description`,`cast`,`coverImage`,`director`, `otherImage` FROM `movie` WHERE `movieTitle` LIKE %s AND `visibility` = 'true' ORDER BY `movieId` DESC", ("%"+search+"%",))

        return list(cursor.fetchall())

    def searchByUser(userId, search):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movieId`, `movieTitle`, `otherImage`, `smallTitle`,`trailer`,`writter`,`Description`,`cast`,`coverImage`,`director`, `otherImage`, (SELECT `visible` FROM `mylist` WHERE `mylist`.`userId` = %s AND `mylist`.`movieId` = mv.`movieId` AND `mylist`.`visible` = 'true') AS mylist FROM `movie` AS mv WHERE `movieTitle` LIKE %s AND `visibility` = 'true' ORDER BY mv.`movieId` DESC", (userId, "%"+search+"%"))

        movies = list(cursor.fetchall())
        
        for i in movies:
    
            if i['mylist'] == 'true':
                i["mylist"] = True
            else:
                i["mylist"] = False
                
        return movies

    def addMylist(user, mvId):
        cursor = db.connection.cursor()
        try:
            cursor.execute("INSERT INTO `mylist`(`userId`, `movieId`) VALUES (%s, %s)", (user, mvId))
            db.connection.commit()
        except:
            return False

        return True

    def delMylist(userId,mylistId):
        cursor = db.connection.cursor()
        try:
            cursor.execute("UPDATE `mylist` SET `visible`='false' WHERE `userId` = %s AND `mylistid` = %s", (userId, mylistId))
            db.connection.commit()
        except:
            return False

        return True

    def delMylistBMId(userId,movieId):
        cursor = db.connection.cursor()
        try:
            cursor.execute("UPDATE `mylist` SET `visible`='false' WHERE `userId` = %s AND `movieId` = %s", (userId, movieId))
            db.connection.commit()
        except:
            return False

        return True
    
    def checkMylist(user, mvId):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `mylist` WHERE `userId`= %s AND `movieId` = %s AND `visible` = 'true'", (user, mvId))

        user = cursor.fetchone()

        try:
            l = len(user)
        except:
            l = 0

        if l > 0:
            return True
        else:
            return False

    def Mylist(user):
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`,`movie`.`coverImage`,`movie`.`otherImage`,`movie`.`trailer`,`mylist`.`mylistid` FROM `mylist` JOIN `movie` ON `mylist`.`movieId` = `movie`.`movieId` WHERE `mylist`.`userId` = %s AND `movie`.`visibility` = 'true' AND `mylist`.`visible` = 'true'", (user,))

        return list(cursor.fetchall())

    def addcontactus(**kwargs):
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO `contact`(`name`, `email`, `phoneNumber`, `message`) VALUES (%s, %s, %s, %s)", (kwargs["name"], kwargs["email"], kwargs["phonenumber"], kwargs["message"]))
        db.connection.commit()
        return True
    
    def vdQuality(movieId, userId):
    
        cursor = db.connection.cursor()
        cursor.execute("SELECT `movievideocat`.`movieCvId`, `movievideocat`.`videoType`, IF (EXISTS (SELECT `movieVideoCatId` FROM `watchaccessvd` WHERE `watchaccessvd`.`movieVideoCatId` = `movievideocat`.`movieCvId` AND `watchaccessvd`.`userId` = %s AND `watchaccessvd`.`movieId` = %s), `movievideocat`.`discount`, `movievideocat`.`price`) as amount, `movievideocat`.`price` as checkPrice FROM `movievideocat` WHERE `movievideocat`.`movieId` = %s AND `movievideocat`.`visible` = 'true'", (userId, movieId, movieId))

        return list(cursor.fetchall())
        
    def toPay(movieCvId, userId):

        cursor = db.connection.cursor()
        cursor.execute("SELECT `movievideocat`.`movieId`, IF (EXISTS (SELECT `movieVideoCatId` FROM `watchaccessvd` WHERE `watchaccessvd`.`movieVideoCatId` = `movievideocat`.`movieCvId` AND `watchaccessvd`.`userId` = %s), `movievideocat`.`discount`, `movievideocat`.`price`) as amount FROM `movievideocat` WHERE `movievideocat`.`movieCvId` = %s AND `movievideocat`.`visible` = 'true'", (userId, movieCvId))

        vdQ = list(cursor.fetchall())
        
        if not len(vdQ) == 0:
            vdQ[0]["userId"] = wordEnc(userId)
            vdQ[0]["movieCvId"] = movieCvId

        return vdQ
    
    def payment(**kwargs):
        cursor = db.connection.cursor()
        
        try:
            cursor.execute("INSERT INTO `payment`(`userId`, `movieId`, `movieVideoCatId`, `price`) VALUES (%s, %s, %s, %s)", (wordDec(kwargs["userId"]), kwargs["movieId"], kwargs["mvCvId"], kwargs["price"]))
            db.connection.commit()
        except:
            return False

        if addWatchAccess(**kwargs):
           return True

    def getAvailableForMv(movieId, userId):
    
        cursor = db.connection.cursor()
        cursor.execute("SELECT `watchAccessVdId`, `movieVideoCatId`, `expDate` FROM `watchaccessvd` WHERE `userId` = %s AND `movieId` = %s AND `active` = 'true' ORDER BY `movieVideoCatId` DESC", (userId, movieId))

        res = list(cursor.fetchall())

        try:
            l = len(res)
        except:
            l = 0

        if l < 1:
            return False
            
        
        for i in res:
            if checkExpTime(i['expDate']):
                return getMvCtDet(int(i['movieVideoCatId']))
            else:
                disAccessW(int(i['watchAccessVdId']))
                return False

    def allGenresWMv(sort):
        allGenres = getGenresO()

        for i in allGenres:
            i['movies'] = moviesByGenreO(i["name"], sort)
        
        return allGenres

    def allGenresWMvByUser(userId,sort):
        allGenres = getGenresO()

        for i in allGenres:
            i['movies'] = moviesByGenreOByUser(userId, i["name"], sort)
        
        return allGenres
    
    def userGetNots(userId):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `notification` WHERE `userId`= %s AND `visible` = 'true'", (userId, ))

        vdQ = list(cursor.fetchall())

        for i in vdQ:
            if not checkUserNotExpTime(i['exp']):
                disActivateUserNotification(i['notificationId'])
                vdQ.remove(i)
            
            if i['type'] == 'mylist':
                i['movieDet'] = getMvDetailsByMvIdNot(i['linkId'])
        return vdQ
    
    def AdduserNotif(userid,**kwargs):
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO `notification`(`userId`, `type`, `linkId`, `description`, `exp`) VALUES (%s, %s, %s, %s, %s)", (userid, kwargs['type'], kwargs['linkId'],kwargs['description'], getUserNotExpTime()))
        db.connection.commit()
        return True

    #Short movie --------------------------------------------------------------------
    def allsMovies():
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `shortmovie` WHERE `visibility` = 'true' ORDER BY `smId` DESC")

        movies = list(cursor.fetchall())

        for i in movies:
            i["genres"] = getGenreBysMvId(i["smId"])

        return movies

    def singlesMovie(id):
        cursor = db.connection.cursor()

        cursor.execute("SELECT * FROM `shortmovie` WHERE `smId` = %s AND `visibility` = 'true'", (id,))

        movies = list(cursor.fetchall())

        if len(movies) != 0:
            movies[0]['gernes'] = getGenreBysMvId(id)

        return movies
    
    def smoviesByGenre(name, sort):
        cursor = db.connection.cursor()

        if sort == 'DESC':
            cursor.execute("SELECT `shortmovie`.`smId`,`shortmovie`.`title`,`shortmovie`.`smallTitle`,`shortmovie`.`description`,`shortmovie`.`cast`,`shortmovie`.`director`, `shortmovie`.`trailer`,`shortmovie`.`writter`,`shortmovie`.`coverImage`,`shortmovie`.`video` FROM `genre` JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` JOIN `shortmovie` ON `genresm`.`smId` = `shortmovie`.`smId` WHERE `genre`.`name` = %s AND `shortmovie`.`visibility` = 'true' ORDER BY `shortmovie`.`smId` DESC", (name,))
        else:
            cursor.execute("SELECT `shortmovie`.`smId`,`shortmovie`.`title`,`shortmovie`.`smallTitle`,`shortmovie`.`description`,`shortmovie`.`cast`,`shortmovie`.`director`, `shortmovie`.`trailer`,`shortmovie`.`writter`,`shortmovie`.`coverImage`,`shortmovie`.`video` FROM `genre` JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` JOIN `shortmovie` ON `genresm`.`smId` = `shortmovie`.`smId` WHERE `genre`.`name` = %s AND `shortmovie`.`visibility` = 'true' ORDER BY `shortmovie`.`smId` ASC", (name,))
            
        return list(cursor.fetchall())

    def allGenresWsMv(sort):
        allGenres = getGenresO()

        for i in allGenres:
            i['movies'] = smoviesByGenreO(i["name"], sort)
        
        return allGenres

    # Otherentvd
    def getBehindScene(id):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `otherentvideo` WHERE `oeVdId` = %s AND `type` = 'Behindscene' AND `visibility`='true' ORDER BY `oeVdId` DESC", (id,))
                  
        return list(cursor.fetchall())

    def searchBehindScene(search):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `otherentvideo` WHERE `type` = 'behindscene' AND (`title` LIKE %s OR `smallTitle` LIKE %s OR `description` LIKE %s) AND `visibility` = 'true'", ("%"+search+"%", "%"+search+"%", "%"+search+"%"))
            
        return list(cursor.fetchall())

    def getBehindScenes():
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `otherentvideo` WHERE `type` = 'Behindscene' AND `visibility`='true' ORDER BY `oeVdId` DESC")
            
        return list(cursor.fetchall())
        
    def documentary(id):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `otherentvideo` WHERE `oeVdId` = %s AND `type` = 'documentary' AND `visibility`='true' ORDER BY `oeVdId` DESC", (id,))
            
        return list(cursor.fetchall())

    def documentaries():
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `otherentvideo` WHERE `type` = 'documentary' AND `visibility`='true' ORDER BY `oeVdId` DESC")
            
        return list(cursor.fetchall())

    def searchDocumentary(search):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `otherentvideo` WHERE `type` = 'documentary' AND (`title` LIKE %s OR `smallTitle` LIKE %s OR `description` LIKE %s) AND `visibility` = 'true'", ("%"+search+"%", "%"+search+"%", "%"+search+"%"))
            
        return list(cursor.fetchall())


def disAccessW(id):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE `watchaccessvd` SET `active`='false' WHERE `watchAccessVdId` = %s", (id,))
    db.connection.commit()


def addWatchAccess(**kwargs):
    cursor = db.connection.cursor()
    
    try:
        cursor.execute("INSERT INTO `watchaccessvd`(`movieId`, `movieVideoCatId`, `userId`, `expDate`) VALUES (%s, %s, %s, %s)", (kwargs["movieId"], kwargs["mvCvId"], wordDec(kwargs["userId"]), models.getMvExpTime()))
        db.connection.commit()
    except:
        return False

    return True

def getMvCtDet(movieCvId):
    
    cursor = db.connection.cursor()
    cursor.execute("SELECT `movieId`, `videoType`, `videoSrc` FROM `movievideocat` WHERE `movieCvId` = %s", (movieCvId,))

    return list(cursor.fetchall())
    


def getGenreByMvId(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT `genre`.`name` FROM `genrem` JOIN `genre` ON `genrem`.`genreId` = `genre`.`genreId` WHERE `genrem`.`movieId` = %s AND `genre`.`visible` = 'true'", (id,))

    return [x['name'] for x in list(cursor.fetchall())]

def getGenreBysMvId(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT `genre`.`name` FROM `genresm` JOIN `genre` ON `genresm`.`genreId` = `genre`.`genreId` WHERE `genresm`.`smId` = %s AND `genre`.`visible` = 'true'", (id,))
    data = list(cursor.fetchall())
    array_data=[]

    try:
        l = len(data)
    except:
        l = 0

    if l > 0:
        
        for i in data:
            array_data.append(i['name'])
        
        return array_data
    else:
        return array_data

def getGenresO():
        cursor = db.connection.cursor()
        cursor.execute("SELECT `genreId`, `name` FROM `genre` WHERE `visible` = 'true'")

        return list(cursor.fetchall())

def moviesByGenreO(name, sort):
    cursor = db.connection.cursor()

    if sort == 'DESC':
        cursor.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`,`movie`.`smallTitle`,`movie`.`Description`,`movie`.`cast`,`movie`.`director`,`movie`.`time`,`movie`.`age`,`movie`.`trailer`,`movie`.`writter`,`movie`.`coverImage`,`movie`.`otherImage` FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` ON `genrem`.`movieId` = `movie`.`movieId` WHERE `genre`.`name` = %s AND `movie`.`visibility` = 'true' ORDER BY `movie`.`movieId` DESC;", (name,))
    
    else:
        cursor.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`,`movie`.`smallTitle`,`movie`.`Description`,`movie`.`cast`,`movie`.`director`,`movie`.`time`,`movie`.`age`,`movie`.`trailer`,`movie`.`writter`,`movie`.`coverImage`,`movie`.`otherImage` FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` ON `genrem`.`movieId` = `movie`.`movieId` WHERE `genre`.`name` = %s AND `movie`.`visibility` = 'true' ORDER BY `movie`.`movieId` ASC;", (name,))
        
    return list(cursor.fetchall())

def moviesByGenreOByUser(userId,name, sort):
    cursor = db.connection.cursor()

    if sort == 'DESC':
        cursor.execute("SELECT mv.`movieId`,mv.`movieTitle`,mv.`smallTitle`,mv.`Description`,mv.`cast`,mv.`director`,mv.`time`,mv.`age`,mv.`trailer`,mv.`writter`,mv.`coverImage`,mv.`otherImage`, (SELECT `visible` FROM `mylist` WHERE `mylist`.`userId` = %s AND `mylist`.`movieId` = mv.`movieId` AND `mylist`.`visible` = 'true') AS mylist FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` AS mv ON `genrem`.`movieId` = mv.`movieId` WHERE `genre`.`name` = %s AND mv.`visibility` = 'true' ORDER BY mv.`movieId` DESC;", (userId,name))
    
    else:
        cursor.execute("SELECT mv.`movieId`,mv.`movieTitle`,mv.`smallTitle`,mv.`Description`,mv.`cast`,mv.`director`,mv.`time`,mv.`age`,mv.`trailer`,mv.`writter`,mv.`coverImage`,mv.`otherImage`, (SELECT `visible` FROM `mylist` WHERE `mylist`.`userId` = %s AND `mylist`.`movieId` = mv.`movieId` AND `mylist`.`visible` = 'true') AS mylist FROM `genre` JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` JOIN `movie` AS mv ON `genrem`.`movieId` = mv.`movieId` WHERE `genre`.`name` = %s AND mv.`visibility` = 'true' ORDER BY mv.`movieId` ASC;", (userId,name))
        

    movies = list(cursor.fetchall())
    
    for i in movies:
    
        if i['mylist'] == 'true':
            i["mylist"] = True
        else:
            i["mylist"] = False

    return movies

def smoviesByGenreO(name, sort):
    cursor = db.connection.cursor()

    if sort == 'DESC':
        cursor.execute("SELECT `shortmovie`.`smId`,`shortmovie`.`title`,`shortmovie`.`smallTitle`,`shortmovie`.`description`,`shortmovie`.`cast`,`shortmovie`.`director`, `shortmovie`.`trailer`,`shortmovie`.`writter`,`shortmovie`.`coverImage`,`shortmovie`.`video` FROM `genre` JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` JOIN `shortmovie` ON `genresm`.`smId` = `shortmovie`.`smId` WHERE `genre`.`name` = %s AND `shortmovie`.`visibility` = 'true' ORDER BY `shortmovie`.`smId` DESC;", (name,))
    
    else:
        cursor.execute("SELECT `shortmovie`.`smId`,`shortmovie`.`title`,`shortmovie`.`smallTitle`,`shortmovie`.`description`,`shortmovie`.`cast`,`shortmovie`.`director`, `shortmovie`.`trailer`,`shortmovie`.`writter`,`shortmovie`.`coverImage`,`shortmovie`.`video` FROM `genre` JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` JOIN `shortmovie` ON `genresm`.`smId` = `shortmovie`.`smId` WHERE `genre`.`name` = %s AND `shortmovie`.`visibility` = 'true' ORDER BY `shortmovie`.`smId` ASC;", (name,))
        
    return list(cursor.fetchall())

def disActivateUserNotification(notifId):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE `notification` SET `visible`='false' WHERE `notificationId` = %s", (notifId,))
    db.connection.commit()
    return True

def getMvDetailsByMvIdNot(mvId):
    cursor = db.connection.cursor()
    cursor.execute("SELECT `movieId`,`movieTitle`,`Description`,`coverImage` FROM `movie` WHERE `movieId`= %s AND `visibility` = 'true'", (mvId,))

    return list(cursor.fetchall())