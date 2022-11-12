from models.database import db
from re import S


class Addmovie:
    def __init__(self, Title, SmallTitle, Description, Director, Cast, Written, Time, Age, Genre, CoverImage, OtherImage, Trailer):
        self.mysql = db
        self.Title = Title
        self.SmallTitle = SmallTitle
        self.Description = Description
        self.Director = Director
        self.Cast = Cast
        self.Written = Written
        self.Time = Time
        self.Age = Age
        self.Genre = Genre
        self.CoverImage = CoverImage
        self.OtherImage = OtherImage
        self.Trailer = Trailer

    def addGenre(self, id):
        rows = [(id, genre) for genre in self.Genre]

        cur = self.mysql.connection.cursor()
        cur.executemany("INSERT INTO `genrem`(`movieId`, `genreId`) VALUES (%s, %s)", rows)
        
        self.mysql.connection.commit()
        
    def addmovie(self):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO `movie`(`movieTitle`, `smallTitle`, `Description`, `cast`, `director`, `time`, `age`, `trailer`, `writter`, `coverImage`, `otherImage`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.Title, self.SmallTitle, self.Description, self.Cast, self.Director, self.Time, self.Age, self.Trailer, self.Written, self.CoverImage, self.OtherImage))
        
        id = self.mysql.connection.insert_id()
        self.addGenre(id)

    @classmethod
    def fetchMovie(cls, start, end, genre, sort):

        if int(genre) == 0:

            cur = db.connection.cursor()
            if sort == 'ASC':
                cur.execute("SELECT `movieId`,`movieTitle`, `Description`, `coverImage` FROM `movie` WHERE `visibility`= 'true' ORDER BY `movieId` ASC LIMIT %s, %s;", (start, end))
            else:
                cur.execute("SELECT `movieId`,`movieTitle`, `Description`, `coverImage` FROM `movie` WHERE `visibility`= 'true' ORDER BY `movieId` DESC LIMIT %s, %s;", (start, end))

            return cur.fetchall()

        else:
            cur = db.connection.cursor()

            if sort == 'ASC':
                cur.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`, `movie`.`Description`, `movie`.`coverImage` FROM `genre` INNER JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` INNER JOIN `movie` ON `movie`.`movieId` = `genrem`.`movieId` WHERE `genre`.`genreId` = %s AND `movie`.`visibility`= 'true' ORDER BY `movie`.`movieId` ASC LIMIT %s, %s", (genre, start, end))
            else:
                cur.execute("SELECT `movie`.`movieId`,`movie`.`movieTitle`, `movie`.`Description`, `movie`.`coverImage` FROM `genre` INNER JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` INNER JOIN `movie` ON `movie`.`movieId` = `genrem`.`movieId` WHERE `genre`.`genreId` = %s AND `movie`.`visibility`= 'true' ORDER BY `movie`.`movieId` DESC LIMIT %s, %s", (genre, start, end))
            return cur.fetchall()
    
    @classmethod
    def AllNbrmovie(cls, genre):

        if int(genre) == 0:

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `movie` WHERE `visibility`= 'true';")

            return cur.fetchall()

        else:

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `genre` INNER JOIN `genrem` ON `genre`.`genreId` = `genrem`.`genreId` INNER JOIN `movie` ON `movie`.`movieId` = `genrem`.`movieId` WHERE `genre`.`genreId` = %s AND `movie`.`visibility`= 'true'", (genre,))

            return cur.fetchall()
    
    @classmethod
    def search(cls, search):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `movie` WHERE `movieTitle` LIKE %s AND `movie`.`visibility`= 'true'", ("%"+search+"%",))

        return cur.fetchall()

    @classmethod
    def remove(cls, id):
        cur = db.connection.cursor()
        cur.execute("UPDATE `movie` SET `visibility`= 'false' WHERE `movieId` = %s", (id,))

        db.connection.commit()

    @classmethod
    def oneM(cls, id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `movie` WHERE `movieId` = %s", (id,))

        return cur.fetchall()

    @classmethod
    def updateM(cls, id, title, smtitle, dec, dir, cast, written, time, age, trailer, cimg, himg):
        cur = db.connection.cursor()
        cur.execute("UPDATE `movie` SET `movieTitle`= %s,`smallTitle`= %s,`Description`= %s,`cast`= %s,`director`= %s,`time`= %s,`age`= %s,`trailer`= %s,`writter`= %s,`coverImage`= %s,`otherImage`= %s WHERE `movieId`= %s", (title, smtitle, dec, cast, dir, time, age, trailer, written, cimg, himg, id))

        return cur.connection.commit()


class homeSlides:
    def __init__(self, id, bnt, type):
        self.mysql = db
        self.id = id
        self.bnt = bnt
        self.type = type
    
    def addH(self):

        if self.checkH():
            cur = self.mysql.connection.cursor()
            cur.execute("INSERT INTO `homeslide`(`movieId`, `btnVisible`, `type`) VALUES (%s,%s,%s)", (self.id, self.bnt, self.type))

            self.mysql.connection.commit()
    
    def checkH(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `homeslide` WHERE `movieId` = %s AND `visibility` = 'true'", (self.id,))
        ft = cur.fetchone()

        if not ft:
            return True
        else:
            return False
    
    @classmethod
    def allH(cls):
        cur = db.connection.cursor()
        cur.execute("SELECT `movie`.`movieId`, `movie`.`movieTitle`,`movie`.`coverImage`,`homeslide`.`hmId`,`homeslide`.`btnVisible` FROM `homeslide` INNER JOIN `movie` ON `homeslide`.`movieId` = `movie`.`movieId`  WHERE `homeslide`.`visibility` = 'true' AND `movie`.`visibility` = 'true'")
        return cur.fetchall()

    @classmethod
    def hmBtn(cls, id, btn):
        cur = db.connection.cursor()
        cur.execute("UPDATE `homeslide` SET `btnVisible`= %s WHERE `hmId` = %s", (btn, id))
        db.connection.commit()

    @classmethod
    def hmv(cls, id):
        cur = db.connection.cursor()
        cur.execute("UPDATE `homeslide` SET `visibility`= 'false' WHERE `hmId` = %s", (id,))
        db.connection.commit()

class MovCat:
    def __init__(self, id, price, discount, videoT, Src):
        self.mysql = db
        self.id = id
        self.price = price
        self.discount = discount
        self.videoT = videoT
        self.Src = Src

    def priceAdd(self):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO `movievideocat`(`movieId`, `videoType`, `videoSrc`, `price`, `discount`) VALUES (%s, %s, %s, %s, %s)", (self.id, self.videoT, self.Src, self.price, self.discount))
        self.mysql.connection.commit()
         
    @classmethod
    def viewCat(cls, id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `movievideocat` WHERE `movieCvId` = %s AND `visible` = 'true'", (id,))
        return cur.fetchone()

    @classmethod
    def viewCats(cls, id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `movievideocat` WHERE `movieId` = %s AND `visible` = 'true'", (id,))
        return cur.fetchall()
    
    @classmethod
    def getMovTitle(cls,id):
        cur = db.connection.cursor()
        cur.execute("SELECT `movieTitle` FROM `movie` WHERE `movieId` = %s AND `visibility` = 'true'", (id,))
        return cur.fetchall()

    @classmethod
    def priceUpdate(cls, id, Price, Discount, VideoType, Src):
        cur = db.connection.cursor()
        cur.execute("UPDATE `movievideocat` SET `videoType`=%s,`videoSrc`=%s,`price`=%s,`discount`=%s WHERE `movieCvId`= %s", (VideoType, Src, Price, Discount, id))
        db.connection.commit()
    
    @classmethod
    def delCat(cls, id):
        cur = db.connection.cursor()
        cur.execute("UPDATE `movievideocat` SET `visible`= 'false' WHERE `movieCvId` = %s", (id,))
        db.connection.commit()


class Notification:
    def __init__(self):
        self.mysql = db
    
    def view(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `adminnotification` WHERE `visible` = 'true'")
        return cur.fetchall()

    def updateNot(self):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE `adminnotification` SET `visible` = 'false' WHERE `visible` = 'true'")
        self.mysql.connection.commit()

class contactUs:
    def __init__(self):
        self.mysql = db
    
    def view(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `contact` WHERE `visible` = 'true' ORDER BY `ctUsId` DESC")
        return cur.fetchall()
    
    def delCant(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE `contact` SET `visible`='false]' WHERE `ctUsId` = %s", (id,))
        self.mysql.connection.commit()
    

    

