from models.database import db
from re import S


class Otherentvd:
    def __init__(self, Title, SmallTitle, Description, type, image, video):
        self.mysql = db
        self.Title = Title
        self.SmallTitle = SmallTitle
        self.Description = Description
        self.type = type
        self.image = image
        self.video = video
        
    def addmovie(self):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO `otherentvideo`(`title`, `smallTitle`, `description`, `image`, `video`, `type`) VALUES (%s, %s, %s, %s, %s, %s)", (self.Title, self.SmallTitle, self.Description, self.image, self.video, self.type))
        
        self.mysql.connection.commit()

    @classmethod
    def AllNbrmovie(cls, type):

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `otherentvideo` WHERE `type` = %s AND `visibility` = 'true'", (type,))

            return cur.fetchall()

    @classmethod
    def fetchMovie(cls, start, end, type, sort):

        cur = db.connection.cursor()
        if sort == 'ASC':
            cur.execute("SELECT `oeVdId`, `title`, `smallTitle`, `description`, `image` FROM `otherentvideo` WHERE `type` = %s AND `visibility`='true' ORDER BY `oeVdId` ASC LIMIT %s, %s;", (type, start, end))
        else:
            cur.execute("SELECT `oeVdId`, `title`, `smallTitle`, `description`, `image` FROM `otherentvideo` WHERE `type` = %s AND `visibility`='true' ORDER BY `oeVdId` DESC LIMIT %s, %s;", (type, start, end))

        return cur.fetchall()
    
    @classmethod
    def search(cls, search):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `otherentvideo` WHERE (`title` LIKE %s OR `smallTitle` LIKE %s OR `description` LIKE %s) AND `visibility` = 'true'", ("%"+search+"%", "%"+search+"%", "%"+search+"%"))

        return cur.fetchall()

    @classmethod
    def remove(cls, id):
        cur = db.connection.cursor()
        cur.execute("UPDATE `otherentvideo` SET `visibility`= 'false' WHERE `oeVdId` = %s", (id,))

        db.connection.commit()

    @classmethod
    def oneM(cls, id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `otherentvideo` WHERE `oeVdId` = %s", (id,))

        return cur.fetchall()

    @classmethod
    def updateM(cls, id, title, smtitle, dec, cimg, video):
        cur = db.connection.cursor()
        cur.execute("UPDATE `otherentvideo` SET `title`= %s,`smallTitle`= %s,`description`= %s,`image`= %s,`video`= %s WHERE `oeVdId` = %s", (title, smtitle, dec, cimg, video, id))

        return cur.connection.commit()