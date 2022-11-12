from models.database import db

class appInfo:
    def __init__(self):
        self.mysql = db

    def view(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM `details` WHERE `id` = 1")
        return cur.fetchone()

    def topCDetails(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT COUNT(`movieId`) FROM `movie` WHERE `visibility` = 'true' UNION ALL SELECT COUNT(`genreId`) FROM `genre` WHERE `visible` = 'true' UNION ALL SELECT COUNT(`AdminId`) FROM `adminuser` WHERE `visible` = 'true' UNION ALL SELECT COUNT(`oeVdId`) FROM `otherentvideo` WHERE `visibility` = 'true' UNION ALL SELECT COUNT(`hmId`) FROM `homeslide` WHERE `visibility` = 'true'; ")
        return cur.fetchall()

    def updateInfo(self, loc, phone, email):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE `details` SET `location`= %s,`phoneNumber`= %s,`email`= %s WHERE `id` = 1", (loc, phone, email))
        self.mysql.connection.commit()