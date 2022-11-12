from models.database import db
from re import S


class shortMovie:
    def __init__(self, Title, SmallTitle, Description, Director, Cast, Written, Genre, CoverImage, video, Trailer):
        self.mysql = db
        self.Title = Title
        self.SmallTitle = SmallTitle
        self.Description = Description
        self.Director = Director
        self.Cast = Cast
        self.Written = Written
        self.Genre = Genre
        self.CoverImage = CoverImage
        self.video = video
        self.Trailer = Trailer

    def addGenre(self, id):
        rows = [(id, genre) for genre in self.Genre]

        cur = self.mysql.connection.cursor()
        cur.executemany("INSERT INTO `genresm`(`smId`, `genreId`) VALUES (%s, %s)", rows)
        
        self.mysql.connection.commit()
        
    def addmovie(self):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO `shortmovie`(`title`, `smallTitle`, `description`, `cast`, `director`, `trailer`, `writter`, `coverImage`, `video`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.Title, self.SmallTitle, self.Description, self.Cast, self.Director, self.Trailer, self.Written, self.CoverImage, self.video))
        
        id = self.mysql.connection.insert_id()
        self.addGenre(id)

    @classmethod
    def fetchMovie(cls, start, end, genre, sort):

        if int(genre) == 0:

            cur = db.connection.cursor()
            if sort == 'ASC':
                cur.execute("SELECT `smId`,`title`, `description`, `coverImage` FROM `shortmovie` WHERE `visibility`= 'true' ORDER BY `smId` ASC LIMIT %s, %s;", (start, end))
            else:
                cur.execute("SELECT `smId`,`title`, `description`, `coverImage` FROM `shortmovie` WHERE `visibility`= 'true' ORDER BY `smId` DESC LIMIT %s, %s;", (start, end))

            return cur.fetchall()

        else:
            cur = db.connection.cursor()

            if sort == 'ASC':
                cur.execute("SELECT `shortmovie`.`smId`,`shortmovie`.`title`, `shortmovie`.`description`, `shortmovie`.`coverImage` FROM `genre` INNER JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` INNER JOIN `shortmovie` ON `shortmovie`.`smId` = `genresm`.`smId` WHERE `genre`.`genreId` = %s AND `shortmovie`.`visibility`= 'true' ORDER BY `shortmovie`.`smId` ASC LIMIT %s, %s", (genre, start, end))
            else:
                cur.execute("SELECT `shortmovie`.`smId`,`shortmovie`.`title`, `shortmovie`.`description`, `shortmovie`.`coverImage` FROM `genre` INNER JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` INNER JOIN `shortmovie` ON `shortmovie`.`smId` = `genresm`.`smId` WHERE `genre`.`genreId` = %s AND `shortmovie`.`visibility`= 'true' ORDER BY `shortmovie`.`smId` DESC LIMIT %s, %s", (genre, start, end))
            return cur.fetchall()
    
    @classmethod
    def AllNbrmovie(cls, genre):

        if int(genre) == 0:

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `shortmovie` WHERE `visibility`= 'true';")

            return cur.fetchall()

        else:

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `genre` INNER JOIN `genresm` ON `genre`.`genreId` = `genresm`.`genreId` INNER JOIN `shortmovie` ON `shortmovie`.`smId` = `genresm`.`smId` WHERE `genre`.`genreId` = %s AND `shortmovie`.`visibility`= 'true'", (genre,))

            return cur.fetchall()
    
    @classmethod
    def search(cls, search):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `shortmovie` WHERE `title` LIKE %s AND `shortmovie`.`visibility`= 'true'", ("%"+search+"%",))

        return cur.fetchall()

    @classmethod
    def remove(cls, id):
        cur = db.connection.cursor()
        cur.execute("UPDATE `shortmovie` SET `visibility`= 'false' WHERE `smId` = %s", (id,))

        db.connection.commit()

    @classmethod
    def oneM(cls, id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM `shortmovie` WHERE `smId` = %s", (id,))

        return cur.fetchall()

    @classmethod
    def updateM(cls, id, title, smtitle, dec, dir, cast, written, trailer, cimg, video):
        cur = db.connection.cursor()
        cur.execute("UPDATE `shortmovie` SET `title`= %s,`smallTitle`= %s,`description`= %s,`cast`= %s,`director`= %s,`trailer`= %s,`writter`= %s,`coverImage`= %s,`video`= %s WHERE `smId`= %s", (title, smtitle, dec, cast, dir, trailer, written, cimg, video, id))

        return cur.connection.commit()