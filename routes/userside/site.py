from distutils.command.build_scripts import first_line_re
from random import random
from traceback import print_tb
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, session
from flask.helpers import make_response
import requests
from werkzeug.utils import secure_filename
import os
from models import genImageName, cache
import random
from werkzeug.datastructures import MultiDict

from constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_500_INTERNAL_SERVER_ERROR

userSide = Blueprint('userside', __name__)


''' Variables '''

#URL = 'http://127.0.0.1:5000/'
URL = 'https://rielen.herokuapp.com/'
UPLOAD_FOLDER = 'static/profiles/users/'

''' end '''

''' ---------------------------------------------------------------------------------------'''

""" User Auth """

@userSide.route('/login', methods=['POST'])
def login():
    ''' session.pop('userInfo')
    session.pop('notification') '''
    session.clear()
    data = request.form

    logReq = requests.post(URL+'/api/v1/login', data=data)
    

    if logReq.status_code == HTTP_200_OK:
         
        resD = logReq.json()
        if resD["message"] == "login successful":
            d = logReq.json()
            d['url'] = data['url']
            res = make_response(jsonify(d), logReq.status_code)

            res.set_cookie('access_token', resD["access_token"])
            res.set_cookie('refresh_token', resD["refresh_token"])
            return res

    
    return make_response(jsonify(logReq.json()), logReq.status_code)



@userSide.route('/register', methods=['POST'])
def register():
    data = request.form

    logReq = requests.post(URL+'/api/v1/register', data=data)

    
    return make_response(jsonify(logReq.json()), logReq.status_code)

    

""" end """

''' ---------------------------------------------------------------------------------------'''



''' Functions '''

def validToken():

    if request.cookies.get('access_token'):

        token = request.cookies.get('access_token')
        headers = {"Authorization": "Bearer "+token}

        req = requests.get(URL+'api/v1/validtoken', headers=headers)

        if req.status_code == HTTP_200_OK:
            return True
        else:
            return False 

    else:
        return False

def refreshToken():
    
    if request.cookies.get('refresh_token'):

        token = request.cookies.get('refresh_token')
        headers = {"Authorization": "Bearer "+token}

        resData = requests.get(URL+'/api/v1/refresh_token', headers=headers)

        if resData.status_code == HTTP_200_OK:
            
            return resData.json()
        
        else:

            return False
    else:

        return False

def check_token_statusCode():
    
    if request.cookies.get('access_token'):
    
        token = request.cookies.get('access_token')
        headers = {"Authorization": "Bearer "+token}

        resData = requests.get(URL+'/api/v1/validtoken', headers=headers)

        return resData.status_code
    
    else:
        return 0

def getUserI():

    if not session.get('userInfo') or session.get('userInfo') == 0:
    
        if request.cookies.get('access_token'):

            token = request.cookies.get('access_token')
            headers = {"Authorization": "Bearer "+token}

            resData = requests.get(URL+'/api/v1/userinfo', headers=headers)

            if resData.status_code == HTTP_401_UNAUTHORIZED:
            
                rT = refreshToken()

                if rT != False:

                    headersT = {"Authorization": "Bearer "+rT["access_token"]}

                    resDatap = requests.get(URL+'/api/v1/userinfo', headers=headersT)

                    if resDatap.status_code == HTTP_200_OK:
                        res = resDatap.json()['data'][0]

                    else:
                        res = 0

                else:
                    res = 0
            
            elif resData.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
                res = 0
            
            elif resData.status_code == HTTP_200_OK:
                res = resData.json()['data'][0]

            else:
                res = 0
                
        else:
            res = 0

        session["userInfo"] = res

        return res
    
    else:

        return session.get('userInfo')

def mylistDt():
    if request.cookies.get('access_token'):

        token = request.cookies.get('access_token')
        header = {"Authorization": "Bearer "+token}
        res  = requests.get(URL+'/api/v1/mylist', headers= header)

        if res.status_code == HTTP_200_OK:
            return res.json()["data"]
        else:
            return False

    else:
        return False

def getNotification():

    if not session.get('notification') or session.get('notification') == 0:

        if request.cookies.get('access_token'):

            token = request.cookies.get('access_token')
            header = {"Authorization": "Bearer "+token}
            res  = requests.get(URL+'/api/v1/notification', headers= header)

            if res.status_code == HTTP_200_OK or res.status_code == HTTP_404_NOT_FOUND:
                Not = res.json()["data"]
            else:
                Not = False

        else:
            Not = False

        session["notification"] = Not

        return Not
    else:

        return session.get('notification')

def homeSlidesF():

    if not session.get('homeslides') or session.get('homeslides') == 0:
        resHM = requests.get(URL+'/api/v1/homeslides')

        if resHM.status_code == HTTP_200_OK:
            resHM = resHM.json()
        else:
            resHM = {
                "data": [{
                        "Description": "When a mysterious woman seduces Dominic Toretto into the world of terrorism and a betrayal of those closest to him, the crew face trials that will test them as never before.",
                        "btnVisible": "true",
                        "coverImage": "wp2465015-the-fate-of-the-furious-wallpapers.jpg",
                        "movieId": "gAAAAABiJ5InhFY4Nfr81uJ2hDjiGqbhlj8yzK9DSfC5EPiJPj_bwYc0VbEIwSN1Gl6I4M0qY1phOWPNt0y1b7o_05Wn5NZeew==",
                        "movieTitle": "The Fate of the Furious",
                        "type": "image"}]
                    }
        session["homeslides"] = resHM
        return resHM
    else:

        return session.get('homeslides')

@cache.cached(timeout=86400, key_prefix='genresFun')
def genresFun():

    res = requests.get(URL+'/api/v1/genres')

    if res.status_code == HTTP_200_OK:
        res = res.json()['data']
    else:
        res = [{'date': 'Sat, 13 Nov 2021 21:47:40 GMT', 'genreId': 'gAAAAABiK86ORLEhnLVleBEXK6kiqTgdA2YWR9uWyiU7X7MS1N0s0Xdl86MTu8N8UPsf1MlTZpWvKbTQfDnsmuSdsHq9U-DtZw==', 'name': 'romantic', 'visible': 'true'}, {'date': 'Sat, 13 Nov 2021 22:18:16 GMT', 'genreId': 'gAAAAABiK86On0zhVKiSnQCU5Hp8eUollHgIXKrwPBP38nYDlKUI4jP1io6r6jUUftIdyqq9JfD90kmQ41tYJI2kq_YexgCV7A==', 'name': 'sci-fi', 'visible': 'true'}, {'date': 'Sun, 30 Jan 2022 14:59:22 GMT', 'genreId': 'gAAAAABiK86O323TACkdQPYdfI6DIkQyAYHeINeeYuoPGuOohOOzAj-DnSFx0DWiGDGQ7KWreCNVWooPSH6JQ7MvyAseKOlfvg==', 'name': 'action', 'visible': 'true'}, {'date': 'Sun, 30 Jan 2022 14:59:41 GMT', 'genreId': 'gAAAAABiK86OWzHe48K8j_5a1xU97-yC-kQE9k8kcxFjMtWYYKslIeGwdjcjYGBwAZb92i-q6zNuIbWOpzMn_hZhCljdE8rVUQ==', 'name': 'comedy', 'visible': 'true'}]
    print(res)
    return res


def checkInMlist(movieId):
    if request.cookies.get('access_token'):
        token = request.cookies.get('access_token')
        header = {"Authorization": "Bearer "+token}
        res  = requests.post(URL+'/api/v1/mylistcheck', headers= header, params={'movieid': movieId})

        if res.status_code == HTTP_200_OK:
            return res.json()['message']
        else:
            return False
    else:
        return False

def genclassname(a, b, c, d, e):
    s = a[0:2]+ b[-1] + c[0:2] + d[-1] + b[0:2] + a[0] + c[-1] + d[0:2] + e[0:2] + a[-1] +e[-1]

    for i in ['.', ' ', '  ', '$', '@', '!', '%', '?', '#', '$', '+', '-', '(', ')', '|']:
        s = s.replace(i, 'A')
    return s

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

''' end '''



''' ---------------------------------------------------------------------------------------'''


""" Movie """
@userSide.route('/', methods=['GET'])
@userSide.route('/home', methods=['GET'])
def home():
    status_code = check_token_statusCode()

    resHM = homeSlidesF()

    if status_code == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if not rT:
            restpMv= requests.get(URL+'/api/v1/movies').json()
            restGWMv= requests.get(URL+'/api/v1/genresWithMovies').json()
            return render_template('userside/index.html', hmsl = resHM, tpMv = restpMv['data'][0], restGWMv = restGWMv['data'], user = 0, mylist = checkInMlist, notification = False, genclass = genclassname)

        else:
            mResp = make_response( redirect( url_for('userside.home') ) )
            mResp.set_cookie("access_token", rT["access_token"])
            mResp.set_cookie("refresh_token", rT["refresh_token"])

            return mResp

    if status_code == HTTP_200_OK:

        token = request.cookies.get('access_token')
        headers = {"Authorization": "Bearer "+token}

        restpMv= requests.get(URL+'/api/v1/moviesbyuser', headers=headers)
        restGWMv= requests.get(URL+'/api/v1/genresWithMoviesbyuser', headers=headers)

        if restpMv.status_code == HTTP_200_OK:
            restpMv = restpMv.json()
        else:
            restpMv = requests.get(URL+'/api/v1/movies').json()

        if restGWMv.status_code == HTTP_200_OK:
            restGWMv = restGWMv.json()
        else:
            restGWMv = requests.get(URL+'/api/v1/genresWithMovies').json()
    else:

        restpMv= requests.get(URL+'/api/v1/movies').json()
        restGWMv= requests.get(URL+'/api/v1/genresWithMovies').json()


    if status_code == HTTP_200_OK:
        return render_template('userside/index.html', hmsl = resHM, tpMv = restpMv['data'][0], restGWMv = restGWMv['data'], user = getUserI(), mylist = checkInMlist, notification = getNotification(), genclass = genclassname)
    else:
        return render_template('userside/index.html', hmsl = resHM, tpMv = restpMv['data'][0], restGWMv = restGWMv['data'], user = 0, mylist = checkInMlist, notification = False, genclass = genclassname)


@userSide.route('/movie', methods=['GET'])
def movie():

    if request.args.get('genre') and request.args.get('genre') != '':
        genre = request.args.get('genre')
    else:
        genre = 'all'

    if request.args.get('sort'):
        sort = request.args.get('sort')
    else:
        sort= 'DESC'
    
    status_code = check_token_statusCode()

    if status_code == HTTP_401_UNAUTHORIZED:
    
        rT = refreshToken()

        if rT != False:

            mResp = make_response( redirect( url_for('userside.movie', genre=genre, sort=sort) ) )
            mResp.set_cookie("access_token", rT["access_token"])
            mResp.set_cookie("refresh_token", rT["refresh_token"])

            return mResp

    if genre == 'all':
        
        if status_code == HTTP_200_OK:
    
            token = request.cookies.get('access_token')
            headers = {"Authorization": "Bearer "+token}

            resHM= requests.get(URL+'/api/v1/genresWithMoviesbyuser', headers=headers, params={'sort': sort})

            if resHM.status_code == HTTP_200_OK:
                resHM = resHM.json()
            else:
                resHM = requests.get(URL+'/api/v1/genresWithMovies', params={'sort': sort}).json()

        else:
            resHM = requests.get(URL+'/api/v1/genresWithMovies', params={'sort': sort}).json()
        
        Mov_res = {'categ': 'all', 'data': resHM['data']}
    
    else:

        if status_code == HTTP_200_OK:
        
            token = request.cookies.get('access_token')
            headers = {"Authorization": "Bearer "+token}

            resHM= requests.get(URL+'/api/v1/moviesbygenrebyuser/'+genre, headers=headers, params={'sort': sort})

            if resHM.status_code == HTTP_200_OK:
                resHM = resHM.json()
            else:
                resHM = requests.get(URL+'/api/v1/moviesbygenre/'+genre, params={'sort': sort}).json()

        else:
            resHM = requests.get(URL+'/api/v1/moviesbygenre/'+genre, params={'sort': sort}).json()

        Mov_res = {'categ': genre, 'data': resHM['data']}

    
    genres = genresFun()

    if status_code == HTTP_401_UNAUTHORIZED:
        rT = refreshToken()
        if not rT:
            return render_template('userside/movie.html', user = 0, mylist = checkInMlist, mov_res = Mov_res, genres = genres, genclass = genclassname, notification = False)

    if status_code == HTTP_200_OK:
        return render_template('userside/movie.html', user = getUserI(), mylist = checkInMlist, mov_res = Mov_res, genres = genres, genclass = genclassname, notification = getNotification())
    else:
        return render_template('userside/movie.html', user = 0, mylist = checkInMlist, mov_res = Mov_res, genres = genres, genclass = genclassname, notification = False)

@userSide.route('/logout', methods=['GET'])
def logout():
    session.clear()
    path = request.args.get('path')

    res = make_response(redirect(path)) #url_for('userside.home')

    res.delete_cookie('access_token')
    res.delete_cookie('refresh_token')
    return res
        

@userSide.route('/me', methods=['GET', 'POST'])
def userMinfo():

    status_code = check_token_statusCode()
    if status_code == HTTP_401_UNAUTHORIZED:
    
        rT = refreshToken()

        if not rT:
            return render_template('userside/personinfo.html', user = 0, notification = False)
        
        if request.args.get('change'):

            mResp = make_response( redirect( url_for('userside.userMinfo', change = request.args.get('change')) ) )
        
        else:
            mResp = make_response( redirect( url_for('userside.userMinfo') ) )

        mResp.set_cookie("access_token", rT["access_token"])
        mResp.set_cookie("refresh_token", rT["refresh_token"])

        return mResp
    
    if request.method == 'POST':

        token = request.cookies.get('access_token')
        headers = {"Authorization": "Bearer "+token}

        if 'newPassw' not in request.form:
            
            data = request.form
            

            if 'profile' in request.files:

                file = request.files['profile']
                
                if file.filename != '' and file and allowed_file(file.filename):

                    filename = genImageName(secure_filename(file.filename))
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    f = filename
                
                else:
                    f = data['prof']
            else:
                f = data['prof']
                
            json_data = {
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'username': data['username'],
                'PhoneNumber': data['PhoneNumber'],
                'profile': f,
                'password': data['password'],
            }

            resData = requests.patch(URL+'/api/v1/userinfo', data=json_data, headers=headers)

            if resData.status_code == HTTP_200_OK:
                session.clear()
            resData = resData.json()
            flash(resData['message'], resData['type'])
        
        else:

            data = request.form

            resData = requests.patch(URL+'/api/v1/changepassword', data=data, headers=headers).json()
            flash(resData['message'], resData['type'])
            return redirect(url_for('userside.userMinfo', change='password'))


    if status_code == HTTP_200_OK:
        return render_template('userside/personinfo.html', user = getUserI(), notification = getNotification())
    else:
        return render_template('userside/personinfo.html', user = 0, notification = False)

@userSide.route('/search', methods=['GET'])
def search():

    status_code = check_token_statusCode()

    if status_code == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if rT != False:

            mResp = make_response( redirect( url_for('userside.search') ) )

            mResp.set_cookie("access_token", rT["access_token"])
            mResp.set_cookie("refresh_token", rT["refresh_token"])

            return mResp

    if request.args.get('query'):
        query = request.args.get('query')

        if query == '':
            query = ' '
    else:
            query = ' '

    if status_code == HTTP_200_OK:
    
        token = request.cookies.get('access_token')
        headers = {"Authorization": "Bearer "+token}

        res= requests.get(URL+'/api/v1/searchbyuser/'+str(query), headers=headers)

        if res.status_code == HTTP_200_OK:
            res = res.json()['data']
        else:
            res = requests.get(URL+'/api/v1/search/'+str(query)).json()['data']
    else:
        res = requests.get(URL+'/api/v1/search/'+str(query)).json()['data']
    
    if status_code == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if not rT:
            return render_template('userside/search.html', user = 0, search = res, mylist = checkInMlist, genclass = genclassname, notification = False)
    
    if status_code == HTTP_200_OK:
        return render_template('userside/search.html', user = getUserI(), search = res, mylist = checkInMlist, genclass = genclassname, notification = getNotification())
    else:
        return render_template('userside/search.html', user = 0, search = res, mylist = checkInMlist, genclass = genclassname, notification = False)

@userSide.route('/about', methods=['GET'])
def about():

    return render_template('userside/about.html', user = getUserI(), notification = getNotification())

@userSide.route('/contactus', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        res = requests.post(URL+'/api/v1/contactus', data = request.form)

    return render_template('userside/contact.html', user = getUserI(), notification = getNotification())

@userSide.route('/quality/<string:id>', methods=['GET'])
def quality(id):
    status_code = check_token_statusCode()

    if not status_code and status_code == HTTP_500_INTERNAL_SERVER_ERROR:
        return render_template('userside/quality.html', user = 0, ql = [], movieTitle = '', notification = False)
        
    if status_code == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if not rT:
            return render_template('userside/quality.html', user = 0, ql = [], movieTitle = '', notification = False)

        else:
            mResp = make_response( redirect( url_for('userside.quality', id = id) ) )

            mResp.set_cookie("access_token", rT["access_token"])
            mResp.set_cookie("refresh_token", rT["refresh_token"])

            return 
    
    token = request.cookies.get('access_token')
    headers = {"Authorization": "Bearer "+token}

    getQualities = requests.get(URL+'/api/v1/videoquality/'+id, headers=headers)

    if getQualities.status_code == HTTP_200_OK:
        getQualitiesR = getQualities.json()['data']
    else:
        getQualitiesR = []

    movieTitle = requests.get(URL+'/api/v1/movie/'+id, headers=headers)

    if movieTitle.status_code == HTTP_200_OK:

        movieTitleR = movieTitle.json()['data'][0]['movieTitle']
    else:
        movieTitleR = 'Unkown movie'

    return render_template('userside/quality.html', user = getUserI(), ql = getQualitiesR, movieTitle = movieTitleR, notification = getNotification())

@userSide.route('/watch/<string:id>', methods=['GET'])
def watch(id):

    if request.cookies.get('access_token'):

        status_code = check_token_statusCode()
        if status_code == HTTP_401_UNAUTHORIZED:
            
            rT = refreshToken()

            if not rT:
                return render_template('userside/watch.html', user = 0, bad = True, notification = False)

            else:
                mResp = make_response( redirect( url_for('userside.watch', id = id) ) )

                mResp.set_cookie("access_token", rT["access_token"])
                mResp.set_cookie("refresh_token", rT["refresh_token"])

                return mResp

        token = request.cookies.get('access_token')
        headers = {"Authorization": "Bearer "+token}

        resData = requests.get(URL+'/api/v1/movie/'+id)

        if resData.status_code == HTTP_400_BAD_REQUEST:
            
            return render_template('userside/watch.html', user = getUserI(), bad = True, notification = getNotification())
        
        if status_code == HTTP_200_OK:

            chMvPaid = requests.get(URL+'/api/v1/getmovievideosrc/'+id, headers=headers)

            if chMvPaid.status_code == HTTP_400_BAD_REQUEST:

                return redirect( url_for('userside.quality', id = id) )

    return render_template('userside/watch.html', user = getUserI(), bad = False, notification = getNotification())

@userSide.route('/removemylist/<string:id>', methods=["DELETE"])
def removemylist(id):
    
    status_code = check_token_statusCode()
    if status_code == HTTP_200_OK:
        par = {'mylistid': id}
        movieT = request.cookies.get('access_token')
        movieheader = {"Authorization": "Bearer "+movieT}
        res  = requests.delete(URL+'/api/v1/mylist', headers= movieheader, params=par)

        if res.status_code == HTTP_200_OK:
            return res.json()
        else:
            return make_response({"msg": "Something went wrong"}, HTTP_400_BAD_REQUEST)
    else:
        return make_response({"msg": "Token has expired"}, HTTP_400_BAD_REQUEST)

@userSide.route('/getseminame/<string:id>', methods=["GET"])
def getseminame(id):
    
    res  = requests.get(URL+'/api/v1/movie/'+id)

    if res.status_code == HTTP_200_OK:
        x = res.json()['data'][0]
        t = genclassname(x['movieTitle'], x['Description'], x['director'], x['cast'], x['writter'])
        return make_response({'data': t}, HTTP_200_OK)
    return make_response({'data': ''}, HTTP_200_OK)

@userSide.route('/resMvInMylist/<string:id>', methods=["GET"])
def resMvInMylist(id):
    
    if not checkInMlist(id):
        return make_response({'mssg': False}, HTTP_200_OK)
    else:
        return make_response({'mssg': True}, HTTP_200_OK)


@userSide.route('/mylist', methods=['GET', 'POST', 'DELETE'])
def mylist():

    if request.cookies.get('access_token'):

        token = request.cookies.get('access_token')
        header = {"Authorization": "Bearer "+token}
        res  = requests.get(URL+'/api/v1/mylist', headers= header)

        if res.status_code == HTTP_401_UNAUTHORIZED:

            rT = refreshToken()
            

            if not rT:
                return render_template('userside/mylist.html', user = 0, mylistItems = False, mylist = checkInMlist, notification = False)

            if request.args.get('movieId'):

                mResp = make_response( redirect( url_for('userside.mylist', movieId = request.args.get('movieId')) ) )
            else:
                mResp = make_response( redirect( url_for('userside.mylist') ) )

            mResp.set_cookie("access_token", rT["access_token"])
            mResp.set_cookie("refresh_token", rT["refresh_token"])

            return mResp
            

        elif res.status_code == HTTP_200_OK:

            res = res.json()["data"]
        
        else:
            res = False
        

        if request.method == 'POST':

            if request.form['movieId']:

                movieId = request.form['movieId']
                par = {'movieid': movieId}
                movieT = request.cookies.get('access_token')
                movieheader = {"Authorization": "Bearer "+movieT}
                res  = requests.post(URL+'/api/v1/mylist', headers= movieheader, params=par)

                return res.json()
            return jsonify({'action': 'failed'})


    else:
        res = False

    return render_template('userside/mylist.html', user = getUserI(), mylistItems= res, mylist = checkInMlist, notification = getNotification())


@userSide.route('/sendactivationlink', methods=['GET', 'POST'])
def sendactivationlink():


    mess = ''
    succ = False
    data = []

    if request.args.get('token'):
        userIdToken = request.args.get('token')
        req = requests.get(URL+'/api/v1/resendLink/'+userIdToken)

        if req.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
            mess = "We couldn't found Token"

        if req.status_code == HTTP_200_OK:
            data = req.json()['data']
            succ = True

        if req.status_code == HTTP_400_BAD_REQUEST:
            mess = req.json()['message']

    else:
        mess = "We couldn't found Token"

    

    return render_template('userside/resend.html', user = getUserI(), mess = mess, data = data, succ = succ, notification = getNotification())

@userSide.route('/activate', methods=['GET', 'POST'])
def activate():


    mess = ''
    succ = False

    if request.args.get('token'):
        userIdToken = request.args.get('token')
        req = requests.get(URL+'/api/v1/activate/'+userIdToken)

        if req.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
            mess = "Server error"

        if req.status_code == HTTP_200_OK:
            succ = True

        if req.status_code == HTTP_400_BAD_REQUEST:
            mess = req.json()['message']

    else:
        mess = "We couldn't found Token"

    

    return render_template('userside/activate.html', user = getUserI(), mess = mess, succ = succ, notification = getNotification())

@userSide.route('/forget', methods=['GET', 'POST'])
def forget():

    succ = False
    email = ''
    if request.method == 'POST':
        email = request.form['email']
        data = {"email": email}
        req = requests.post(URL+'/api/v1/sendresetpassw', params = data)

        if req.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
            flash("There are some error", 'error')

        if req.status_code == HTTP_200_OK:
            succ = True
        
        if req.status_code == HTTP_404_NOT_FOUND:
            flash("We couldn't found email you entered, please rewrite your email correctly", 'error')

    return render_template('userside/forget.html', user = getUserI(), succ = succ, email = email, notification = getNotification())

@userSide.route('/resetpassw', methods=['GET', 'POST'])
def resetpassword():

    succ = False
    
    if request.method == 'POST':

        passw = request.form["password"]
        cpassw = request.form["cpassword"]
        user = request.form["user"]
        token = request.form["token"]

        data = {"password": passw, "cpassword": cpassw}

        req = requests.post(URL+'/api/v1/resetUserPassw?user='+user+'&token='+token, params = data)

        if req.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
            flash("There are some error", 'error')

        if req.status_code == HTTP_200_OK:
            return render_template('userside/resetpassword.html', user = getUserI(), succ = True, notification = getNotification())

        if req.status_code == HTTP_400_BAD_REQUEST:
            flash(req.json()['message'], 'error')

        return redirect( url_for('userside.resetpassword', user = user, token = token) ) 

        
    return render_template('userside/resetpassword.html', user = getUserI(), succ = succ, notification = getNotification())

@userSide.route('/shortmovie', methods=['GET'])
def shortmovie():

    if request.args.get('genre') and request.args.get('genre') != '':
        genre = request.args.get('genre')
    else:
        genre = 'all'

    if request.args.get('sort'):
        sort = request.args.get('sort')
    else:
        sort= 'DESC' 
    
    status_code = check_token_statusCode()

    if status_code == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if rT != False:

            mResp = make_response( redirect( url_for('userside.shortmovie', genre=genre, sort=sort) ) )
            mResp.set_cookie("access_token", rT["access_token"])
            mResp.set_cookie("refresh_token", rT["refresh_token"])

            return mResp

    if genre == 'all':
    
        resHM = requests.get(URL+'/api/v1/genresWithsMovies', params={'sort': sort}).json()
        Mov_res = {'categ': 'all', 'data': resHM['data']}
    
    else:

        resHM = requests.get(URL+'/api/v1/smoviesbygenre/'+genre, params={'sort': sort}).json()
        Mov_res = {'categ': genre, 'data': resHM['data']}

    
    genres = genresFun()

    if status_code == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if not rT:
            return render_template('userside/shortmovie.html', user = 0, mov_res = Mov_res, genres = genres, notification = False)

    if status_code == HTTP_200_OK:
        return render_template('userside/shortmovie.html', user = getUserI(), mov_res = Mov_res, genres = genres, notification = getNotification())
    else:
        return render_template('userside/shortmovie.html', user = 0, mov_res = Mov_res, genres = genres, notification = False)
        
@userSide.route('/watch/shortmovie/<string:id>', methods=['GET'])
def watchshortmovie(id):

    return render_template('userside/watch.html', user = getUserI(), notification = getNotification())

@userSide.route('/behindscene', methods=['GET'])
def behindscenes():

    if check_token_statusCode() == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if not rT:
            return redirect( url_for('userside.behindscenes'))

        mResp = make_response( redirect( url_for('userside.behindscenes') ) )
        mResp.set_cookie("access_token", rT["access_token"])
        mResp.set_cookie("refresh_token", rT["refresh_token"])

        return mResp

    if request.args.get('id'):
        sres = requests.get(URL+'/api/v1/behindscene/'+request.args.get('id'))
        if sres.status_code == HTTP_200_OK:
            if len(sres.json()['data']) !=0:
                sres = sres.json()['data'][0]
            else:
                sres = []
        else:
            sres = []
    else: 
        sres = []

    if not request.args.get('search'):
        data = requests.get(URL+'/api/v1/behindscene')
    else:
        data = requests.get(URL+'/api/v1/searchBehindScene/'+request.args.get('search'))

    if data.status_code == HTTP_200_OK:
        dat = data.json()['data']
    else:
        dat = []

    return render_template('userside/otherentvd.html', user = getUserI(), notification = getNotification(), res = dat, sres = sres)

@userSide.route('/documentary', methods=['GET'])
def documentary():

    if check_token_statusCode() == HTTP_401_UNAUTHORIZED:
        
        rT = refreshToken()

        if not rT:
            return redirect( url_for('userside.behindscenes'))

        mResp = make_response( redirect( url_for('userside.behindscenes') ) )
        mResp.set_cookie("access_token", rT["access_token"])
        mResp.set_cookie("refresh_token", rT["refresh_token"])

        return mResp

    if request.args.get('id'):
        sres = requests.get(URL+'/api/v1/documentary/'+request.args.get('id'))
        if sres.status_code == HTTP_200_OK:
            if len(sres.json()['data']) !=0:
                sres = sres.json()['data'][0]
            else:
                sres = []
        else:
            sres = []
    else: 
        sres = []

    if not request.args.get('search'):
        data = requests.get(URL+'/api/v1/documentaries')
    else:
        data = requests.get(URL+'/api/v1/searchDocumentary/'+request.args.get('search'))

    if data.status_code == HTTP_404_NOT_FOUND:
        dat = []
    else:
        dat = data.json()['data']

    return render_template('userside/documentary.html', user = getUserI(), notification = getNotification(), res = dat, sres = sres)

@userSide.route('/terms', methods=['GET', 'POST'])
def terms():

    return render_template('userside/terms.html', user = getUserI(), notification = getNotification())

@userSide.route('/privacy', methods=['GET', 'POST'])
def privacy():

    return render_template('userside/privacy.html', user = getUserI(), notification = getNotification())


""" Handling error """

@userSide.app_errorhandler(HTTP_404_NOT_FOUND)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('userside/notfound.html'), HTTP_404_NOT_FOUND

@userSide.app_errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('userside/servererror.html'), HTTP_500_INTERNAL_SERVER_ERROR

""" end """


