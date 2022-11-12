from flask import Blueprint, redirect, render_template, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re   
import os
import random
from werkzeug.utils import secure_filename
from models.admin import *
import models.database
from models.encordec.cryword import *
from models.email.admin import sendActivationEmailAdmin

admin = Blueprint('admin', __name__, url_prefix='/admin')
#tpDet = appInfo().topCDetails()

@admin.route('/')
def index():
    if not checkSession():
        return redirect(url_for('admin.login'))

    return render_template('/admin/index.html', user = getUserInfo(session['userId']).getuser(), tpDet = appInfo().topCDetails())

@admin.route('/appinfo', methods = ['GET', 'POST'])
def appinfo():
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        Location = request.form["Location"]
        PhoneNumber = request.form["PhoneNumber"]
        Email = request.form["Email"]
        appInfo().updateInfo(Location, PhoneNumber, Email)

    view = appInfo().view()

    return render_template('admin/appinfo.html', user = getUserInfo(session['userId']).getuser(), view = view, tpDet = appInfo().topCDetails())

@admin.route('/user', methods = ['GET', 'POST'])
def user():
    if not checkSession():
        return redirect(url_for('admin.login'))

    user =getUserInfo(session['userId']).getuser()
    UPLOAD_FOLDER = 'static/profiles/admin/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    if request.method == 'GET':
        return render_template('admin/user.html', user = user, tpDet = appInfo().topCDetails())
    else:
        
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if 'updateUserInfo' in request.form:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            phoneNumber = request.form['phoneNumber']
            confirmpassword = request.form['confirmpassword']
            file =''

            #confirmpassword = generate_password_hash(confirmpassword)
            if check_password_hash(str(user[6]), confirmpassword):

                if 'profileImage' in request.files:

                    file = request.files['profileImage']
                    if file.filename == '':
                        file = user[7]
                        updateUserInfo(user[0],firstname, lastname, phoneNumber, file).update()
                    else:
                        if allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(UPLOAD_FOLDER, filename))
                            updateUserInfo(user[0],firstname, lastname, phoneNumber, file.filename).update()
                        else:
                            file = user[7]
                            updateUserInfo(user[0],firstname, lastname, phoneNumber, file).update()
                else:
                    file = user[7]
                    updateUserInfo(user[0],firstname, lastname, phoneNumber, file).update()
            else:
                flash('Uncorrect current password', 'userinfo')
        else:
            cpassw = request.form['Cupassword']
            npassw = request.form['NNpassword']
            CCpassw = request.form['CCpassword']
            passreg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

            if check_password_hash(str(user[6]), cpassw):
                if npassw == CCpassw:
                    mat = re.search(re.compile(passreg), npassw)
                    if mat:
                        n = generate_password_hash(npassw)
                        setNewPassw(n, user[0]).setnewpass()
                        flash('Password change', 'changepass') 
                    else:
                        flash('Password must have Number, Capital letter, small letter and symbols', 'changepass')
                    
                else:
                    flash('Your passwords are not the same', 'changepass')
            else:
                    flash('Uncorrect current password', 'changepass')    

        return redirect(url_for('admin.user'))

@admin.route('/payment')
def payment():
    if not checkSession():
        return redirect(url_for('admin.login'))

    return render_template('admin/payment.html', user = getUserInfo(session['userId']).getuser(), tpDet = appInfo().topCDetails())

@admin.route('/notification')
def notification():
    if not checkSession():
        return redirect(url_for('admin.login'))

    noti = Notification().view() 
    Notification().updateNot() 
 
    return render_template('admin/notification.html', user = getUserInfo(session['userId']).getuser(), notis = noti, tpDet = appInfo().topCDetails())

@admin.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    else:
        form = request.form
        email = form['email']
        passw = form['password']

        if Emailcheck(email):

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `adminuser` WHERE `email` =%s", (email,))
            user = cur.fetchone()
            if user:
                if check_password_hash(str(user[6]), passw):

                    if user[10] == 'true':
                        if user[9] == 'false':
                            codegenn = gencode()[:5]
                            sendCodeUser(user[0], codegenn)
                            sendActivationEmailAdmin(email, codegenn)
                            return redirect(url_for('admin.code', userid=wordEnc(user[0]),action='verify'))
                        else:
                            setSession(user[0])
                            return redirect(url_for('admin.index'))
                    else:
                        flash('Your account is disabled')
                        return redirect(url_for('admin.login'))
                else:
                    flash('Password is incorrect')
                    return redirect(url_for('admin.login'))
            else:
                flash('Email is incorrect')
                return redirect(url_for('admin.login'))
        else:
            flash('Email is Invalid')
            return redirect(url_for('admin.login'))

@admin.route('/homeslide', methods=['GET', 'POST'])
def homeslide():
    if not checkSession():
        return redirect(url_for('admin.login'))
    hm = homeSlides.allH()
    return render_template('admin/index.html', user = getUserInfo(session['userId']).getuser(), homeslides = hm, tpDet = appInfo().topCDetails())

@admin.route('/price', methods=['GET', 'POST'])
def price():
    if not checkSession():
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        id = request.form['id']
        Price = request.form['Price']
        Discount = request.form['Discount']
        VideoType = request.form['VideoType']
        Src = request.form['Src']
        MovCat(id, Price, Discount, VideoType, Src).priceAdd()
        
        return redirect( url_for('admin.price', id = id) )
    else:
        id = request.args.get('id')
        if 'pr' in request.args:
            return render_template('admin/price.html', user = getUserInfo(session['userId']).getuser(), tpDet = appInfo().topCDetails())
        else:
            vcat = MovCat.viewCats(id)
            title = MovCat.getMovTitle(id)
            return render_template('admin/viewprice.html', user = getUserInfo(session['userId']).getuser(), vcats = vcat, title = title[0][0], tpDet = appInfo().topCDetails())
        
@admin.route('/pricem', methods=['GET', 'POST'])
def priceM():
    if not checkSession():
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        id = request.form['id']
        Price = request.form['Price']
        Discount = request.form['Discount']
        VideoType = request.form['VideoType']
        Src = request.form['Src']
        MovCat.priceUpdate(id, Price, Discount, VideoType, Src)
        
        return redirect( url_for('admin.movie') )
    else:
        id = request.args.get('id')
        if 'ed' not in request.args:
            MovCat.delCat(id) 
            return redirect( url_for('admin.movie') )
        else:
            vcat = MovCat.viewCat(id)
            return render_template('admin/editprice.html', user = getUserInfo(session['userId']).getuser(), vcat = vcat, tpDet = appInfo().topCDetails())
        
@admin.route('/hms', methods=['GET'])
def hms():
    if not checkSession():
        return redirect(url_for('admin.login'))

    id = request.args.get('id')
    if not 'hmv' in request.args:
        btn = request.args.get('btn')
        homeSlides.hmBtn(id, btn)
    else:
        homeSlides.hmv(id)

    return redirect( url_for('admin.homeslide') )

@admin.route('/genre', methods=['GET', 'POST'])
def genre():
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        genre = request.form['genre']

        cur = db.connection.cursor()
        cur.execute("INSERT INTO `genre`(`name`) VALUES (%s)", (genre,))
        db.connection.commit()

    return render_template('admin/genre.html', user = getUserInfo(session['userId']).getuser(), genres = genreAll(), tpDet = appInfo().topCDetails())

@admin.route('/genre/edit/<string:name>', methods=['GET', 'POST'])
def genreEdit(name):
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        ename = request.form['genre']

        cur = db.connection.cursor()
        cur.execute("UPDATE `genre` SET `name`=%s WHERE `name`=%s", (ename, name))
        db.connection.commit()

        return redirect(url_for('admin.genre'))


    return render_template('admin/genreed.html', user = getUserInfo(session['userId']).getuser(), genrename = name, tpDet = appInfo().topCDetails())

@admin.get('/genre/delete/<string:id>')
def genreDelete(id):
    if not checkSession():
        return redirect(url_for('admin.login'))

    cur = db.connection.cursor()
    cur.execute("UPDATE `genre` SET `visible`='false' WHERE `genreId`=%s", (id,))
    db.connection.commit()

    return redirect(url_for('admin.genre'))

@admin.route('/contactus')
def contactus():
    if not checkSession():
        return redirect(url_for('admin.login'))

    if 'id' in request.args:
        id = request.args.get('id')
        contactUs().delCant(id)

    all = contactUs().view()
    return render_template('admin/contactus.html', user = getUserInfo(session['userId']).getuser(), views = all, tpDet = appInfo().topCDetails())

@admin.route('/adduser', methods = ['GET', 'POST'])
def adduser():
    if not checkSession():
        return redirect(url_for('admin.login'))

    user =getUserInfo(session['userId']).getuser()
    if request.method == 'GET':
        return render_template('admin/adduser.html', user = user, tpDet = appInfo().topCDetails())
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        phonenumber = request.form['phonenumber']
        gender = request.form['gender']
        passw = request.form['passw']
        cpassw = request.form['cpassw']

        addUser = usercheck(firstname, lastname, email, username, phonenumber, gender, passw, cpassw)
        if addUser.insertUser():
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('admin.adduser'))

@admin.route('/movie', methods= ['GET', 'POST'])
def movie():
    if not checkSession():
        return redirect(url_for('admin.login'))

    if request.method == 'GET':
        if 'items' in request.args and 'sort' in request.args and 'genre' in request.args:
            items = int(request.args['items'])
            sort = request.args['sort']
            genre = int(request.args['genre'])
        else:
            items = 5
            sort = 'Desc'
            genre = 0
        
        if 'page' in request.args:
            page = int(request.args['page'])
        else:
            page = 1

        start = (page - 1) * int(items)

        mv = Addmovie.fetchMovie(start, items, genre, sort)
        nMv = len(Addmovie.AllNbrmovie(genre))

        if nMv % items == 0:
            pag = int(nMv / items)
        else:
            pag = int(nMv / items) + 1

        return render_template('admin/movie.html', user = getUserInfo(session['userId']).getuser(), movies = mv, pag = pag, items= items, sort= sort, genre = genre, page = page, genres = genreAll(), search = False, tpDet = appInfo().topCDetails())

    else:
        search = request.form["search"]
        mv = Addmovie.search(search)

        return render_template('admin/movie.html', user = getUserInfo(session['userId']).getuser(), movies = mv, search = True, tpDet = appInfo().topCDetails())
        
@admin.route('/movieDelete/<int:id>', methods = ['GET', 'POST'])
def movieDel(id):
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    Addmovie.remove(id)
    
    return redirect(url_for('admin.movie'))

@admin.route('/movieEdit', methods = ['GET', 'POST'])
def movieEdit():
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    UPLOAD_FOLDER = 'static/mvImages/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'GET':
        id = request.args.get('id')
        mov = Addmovie.oneM(id)
        return render_template('admin/movedit.html', user = getUserInfo(session['userId']).getuser(), mov = mov, id = id, tpDet = appInfo().topCDetails())

    else:
        id = request.form["id"]
        Title = request.form["Title"]
        SmallTitle = request.form["SmallTitle"]
        Description = request.form["Description"]
        Director = request.form["Director"]
        Cast = request.form["Cast"]
        Written = request.form["Written"]
        Time = request.form["Time"]
        Age = request.form["Age"]
        Trailer = request.form["Trailer"]

        if 'CoverImage' in request.files:
            CImg = request.files["CoverImage"]
            if CImg.filename != '':
                if allowed_file(CImg.filename):
                    filenameC = secure_filename(CImg.filename)
                    CImg.save(os.path.join(UPLOAD_FOLDER, filenameC))
                    CImg = CImg.filename
                else:
                    CImg = request.form["HCoverImage"]
            else:
                CImg = request.form["HCoverImage"]
        else:
            CImg = request.form["HCoverImage"]

        if 'OtherImage' in request.files:
            HIMG = request.files["OtherImage"]
            if HIMG.filename != '':
                if allowed_file(HIMG.filename):
                    filenameO = secure_filename(HIMG.filename)
                    HIMG.save(os.path.join(UPLOAD_FOLDER, filenameO))
                    HIMG = HIMG.filename
                else:
                    HIMG = request.form["HOtherImage"]
            else:
                HIMG = request.form["HOtherImage"]
        else:
            HIMG = request.form["HOtherImage"]
        
        Addmovie.updateM(id, Title, SmallTitle, Description, Director, Cast, Written, Time, Age, Trailer, CImg, HIMG)

        return redirect(url_for('admin.movie'))

@admin.route('/addmovie', methods=['GET', 'POST'])
def addmovie():
    if not checkSession():
        return redirect(url_for('admin.login'))

    UPLOAD_FOLDER = 'static/mvImages/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        Title = request.form['Title']
        SmallTitle = request.form['SmallTitle']
        Description = request.form['Description']
        Director = request.form['Director']
        Cast = request.form['Cast']
        Written = request.form['Written']
        Time = request.form['Time']
        Age = request.form['Age']
        Genre = request.form.getlist('Genre')
        Trailer = request.form['Trailer']
        #Genre = ','.join(Genre)
        if 'CoverImage' in request.files:
            CoverImage = request.files['CoverImage']
            OtherImage = request.files['OtherImage']

            if CoverImage.filename != '' and OtherImage.filename != '':
                if allowed_file(CoverImage.filename) and allowed_file(OtherImage.filename):
                    filenameCoverImage = secure_filename(CoverImage.filename)
                    CoverImage.save(os.path.join(UPLOAD_FOLDER, filenameCoverImage))
                    filenameOtherImage = secure_filename(OtherImage.filename)
                    OtherImage.save(os.path.join(UPLOAD_FOLDER, filenameOtherImage))

                    Addmovie(Title, SmallTitle, Description, Director, Cast, Written, Time, Age, Genre, CoverImage.filename, OtherImage.filename, Trailer).addmovie()

    return render_template('admin/addmovie.html', user = getUserInfo(session['userId']).getuser(), genre = genreAll(), tpDet = appInfo().topCDetails())

@admin.route('/addhomeslide', methods=['GET', 'POST'])
def addhomes():
    if not checkSession():
        return redirect(url_for('admin.login'))

    id = request.args.get('id')

    if request.method == 'GET':
        return render_template('admin/hs.html', id = id, tpDet = appInfo().topCDetails())
    else:
        id = request.form["id"]
        btn = request.form["btn"]
        typeW = request.form["typeW"]

        homeSlides(id, btn, typeW).addH()

        return redirect(url_for('admin.homeslide'))

@admin.route('/code', methods = ['GET', 'POST'])
def code():
    if request.method == 'GET':
        return render_template('admin/codesend.html')
    else:
        if request.form['action'] == 'verify':
            if checkcodeUserEnt(wordDec(request.form['user']), request.form['code']):
                setSession(wordDec(request.form['user']))
                return redirect(url_for('admin.index'))
            else:
                flash('Code is not correct')
                return redirect(url_for('admin.code', userid = wordEnc(request.form['user']), action = request.form['action']), tpDet = appInfo().topCDetails())
            
        else:
            if checkcodeUserEnt(session['newPasswUserId'], request.form['code']):
                return redirect(url_for('admin.setpassword'))
            else:
                flash('Code is not correct to')
                return redirect(url_for('admin.code', userid = wordEnc(session['newPasswUserId']), action = request.form['action']))

@admin.route('/sendEmailCode', methods = ['GET', 'POST'])
def sendEmailCode():
    if request.method == 'GET':
        return render_template('admin/email.html')
    else:
        email = request.form['email']
        getid = getUserId(email).getuser()

        if not getid:
            flash('Email not founded')
            return redirect(url_for('admin.sendEmailCode'))
        else:
            codegenn = gencode()[:5]
            sendCodeUser(getid[0], codegenn)
            getUserId(email).disableV()
            sendActivationEmailAdmin(email, codegenn)
            session['newPasswUserId'] = getid[0]
            return redirect(url_for('admin.code', userid = wordEnc(getid[0]), action = 'npassword'))

@admin.route('/setpassword', methods = ['GET', 'POST'])
def setpassword():
    if request.method == 'GET':
        return render_template('admin/password.html')
    else:
        passw = request.form['passw']
        cpassw = request.form['cpassw']

        if passw == cpassw:
            passw = generate_password_hash(passw)
            pas = setNewPassw(passw, session['newPasswUserId']).setnewpass()

            if pas:
                session.pop('newPasswUserId', default=None)
                return redirect(url_for('admin.login'))
            else:
                return redirect(url_for('admin.setpassword'))
            
@admin.route('/logout', methods = ['GET'])
def logout():

    session.pop('userId', default=None)
    return redirect(url_for('admin.login'))




@admin.route('/shortmovie', methods= ['GET', 'POST'])
def shortmovie():
    if not checkSession():
        return redirect(url_for('admin.login'))

    if request.method == 'GET':
        if 'items' in request.args and 'sort' in request.args and 'genre' in request.args:
            items = int(request.args['items'])
            sort = request.args['sort']
            genre = int(request.args['genre'])
        else:
            items = 5
            sort = 'Desc'
            genre = 0
        
        if 'page' in request.args:
            page = int(request.args['page'])
        else:
            page = 1

        start = (page - 1) * int(items)

        mv = shortMovie.fetchMovie(start, items, genre, sort)
        nMv = len(shortMovie.AllNbrmovie(genre))

        if nMv % items == 0:
            pag = int(nMv / items)
        else:
            pag = int(nMv / items) + 1

        return render_template('admin/shortmovie.html', user = getUserInfo(session['userId']).getuser(), movies = mv, pag = pag, items= items, sort= sort, genre = genre, page = page, genres = genreAll(), search = False, tpDet = appInfo().topCDetails())

    else:
        search = request.form["search"]
        mv = shortMovie.search(search)

        return render_template('admin/shortmovie.html', user = getUserInfo(session['userId']).getuser(), movies = mv, search = True, tpDet = appInfo().topCDetails())


@admin.route('/shortmovieDelete/<int:id>', methods = ['GET', 'POST'])
def shortmovieDelete(id):
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    shortMovie.remove(id)
    
    return redirect(url_for('admin.shortmovie'))

@admin.route('/editShortmovie', methods = ['GET', 'POST'])
def editShortmovie():
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    UPLOAD_FOLDER = 'static/smvImages/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'GET':
        id = request.args.get('id')
        mov = shortMovie.oneM(id)
        return render_template('admin/smovedit.html', user = getUserInfo(session['userId']).getuser(), mov = mov, id = id, tpDet = appInfo().topCDetails())

    else:
        id = request.form["id"]
        Title = request.form["Title"]
        SmallTitle = request.form["SmallTitle"]
        Description = request.form["Description"]
        Director = request.form["Director"]
        Cast = request.form["Cast"]
        Written = request.form["Written"]
        video = request.form["video"]
        Trailer = request.form["Trailer"]

        if 'CoverImage' in request.files:
            CImg = request.files["CoverImage"]
            if CImg.filename != '':
                if allowed_file(CImg.filename):
                    filenameC = secure_filename(CImg.filename)
                    CImg.save(os.path.join(UPLOAD_FOLDER, filenameC))
                    CImg = CImg.filename
                else:
                    CImg = request.form["HCoverImage"]
            else:
                CImg = request.form["HCoverImage"]
        else:
            CImg = request.form["HCoverImage"]
        
        shortMovie.updateM(id, Title, SmallTitle, Description, Director, Cast, Written, Trailer, CImg, video)

        return redirect(url_for('admin.shortmovie'))

@admin.route('/addshortmovie', methods=['GET', 'POST'])
def addshortmovie():
    if not checkSession():
        return redirect(url_for('admin.login'))

    UPLOAD_FOLDER = 'static/smvImages/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        Title = request.form['Title']
        SmallTitle = request.form['SmallTitle']
        Description = request.form['Description']
        Director = request.form['Director']
        Cast = request.form['Cast']
        Written = request.form['Written']
        Genre = request.form.getlist('Genre')
        Trailer = request.form['Trailer']
        video = request.form['video']
        #Genre = ','.join(Genre)
        if 'CoverImage' in request.files:
            CoverImage = request.files['CoverImage']

            if CoverImage.filename != '':
                if allowed_file(CoverImage.filename):
                    filenameCoverImage = secure_filename(CoverImage.filename)
                    CoverImage.save(os.path.join(UPLOAD_FOLDER, filenameCoverImage))

                    shortMovie(Title, SmallTitle, Description, Director, Cast, Written, Genre, CoverImage.filename, video, Trailer).addmovie()

    return render_template('admin/addshortmovie.html', user = getUserInfo(session['userId']).getuser(), genre = genreAll(), tpDet = appInfo().topCDetails())
@admin.route('/otherentvd', methods= ['GET', 'POST'])
def otherentvd():
    if not checkSession():
        return redirect(url_for('admin.login'))

    if request.method == 'GET':
        if 'items' in request.args and 'sort' in request.args and 'type' in request.args:
            items = int(request.args['items'])
            sort = request.args['sort']
            type = request.args['type']
        else:
            items = 5
            sort = 'Desc'
            type = 'behindscene'
        
        if 'page' in request.args:
            page = int(request.args['page'])
        else:
            page = 1

        start = (page - 1) * int(items)

        mv = Otherentvd.fetchMovie(start, items, type, sort)
        nMv = len(Otherentvd.AllNbrmovie(type))
 
        if nMv % items == 0:
            pag = int(nMv / items)
        else:
            pag = int(nMv / items) + 1

        return render_template('admin/othervd.html', user = getUserInfo(session['userId']).getuser(), movies = mv, pag = pag, items= items, sort= sort, genre = type, page = page, search = False, tpDet = appInfo().topCDetails())

    else:
        search = request.form["search"]
        mv = Otherentvd.search(search)

        return render_template('admin/othervd.html', user = getUserInfo(session['userId']).getuser(), movies = mv, search = True, tpDet = appInfo().topCDetails())


@admin.route('/otherentvdDelete/<int:id>', methods = ['GET', 'POST'])
def otherentvdDelete(id):
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    Otherentvd.remove(id)
    
    return redirect(url_for('admin.otherentvd'))

@admin.route('/editotherentvd', methods = ['GET', 'POST'])
def editotherentvd():
    if not checkSession():
        return redirect(url_for('admin.login'))
    
    UPLOAD_FOLDER = 'static/otherentvd/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'GET':
        id = request.args.get('id')
        mov = Otherentvd.oneM(id)
        return render_template('admin/othervdedite.html', user = getUserInfo(session['userId']).getuser(), mov = mov, id = id, tpDet = appInfo().topCDetails())

    else:
        id = request.form["id"]
        Title = request.form["Title"]
        SmallTitle = request.form["SmallTitle"]
        Description = request.form["Description"]
        video = request.form["video"]

        if 'CoverImage' in request.files:
            CImg = request.files["CoverImage"]
            if CImg.filename != '':
                if allowed_file(CImg.filename):
                    filenameC = secure_filename(CImg.filename)
                    CImg.save(os.path.join(UPLOAD_FOLDER, filenameC))
                    CImg = CImg.filename
                else:
                    CImg = request.form["HCoverImage"]
            else:
                CImg = request.form["HCoverImage"]
        else:
            CImg = request.form["HCoverImage"]
        
        Otherentvd.updateM(id, Title, SmallTitle, Description, CImg, video)

        return redirect(url_for('admin.otherentvd'))

@admin.route('/addotherentvd', methods=['GET', 'POST'])
def addotherentvd():
    if not checkSession():
        return redirect(url_for('admin.login'))

    UPLOAD_FOLDER = 'static/otherentvd/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        Title = request.form['Title']
        SmallTitle = request.form['SmallTitle']
        Description = request.form['Description']
        type = request.form['type']
        video = request.form['video']

        if 'CoverImage' in request.files:
            CoverImage = request.files['CoverImage']

            if CoverImage.filename != '':
                if allowed_file(CoverImage.filename):
                    filenameCoverImage = secure_filename(CoverImage.filename)
                    CoverImage.save(os.path.join(UPLOAD_FOLDER, filenameCoverImage))

                    Otherentvd(Title, SmallTitle, Description, type, CoverImage.filename, video).addmovie()

    return render_template('admin/addothervd.html', user = getUserInfo(session['userId']).getuser(), genre = genreAll(), tpDet = appInfo().topCDetails())

