from flask_mail import Message
from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
import models
from constants.http_status_codes import *
from models.admin.otherentvd import Otherentvd
from models.encordec.cryword import wordDec, wordEnc
from .userAuth import api

class homeSlides(Resource):
    
    def get(self):

        data = models.userFetch.homeslides()
        #return make_response({"message": 'success', "data" : data}, HTTP_200_OK)
        return make_response({"message": "success","data" :data}, HTTP_200_OK)


class allMovies(Resource):
    
    def get(self):

        data = models.userFetch.allMovies()
        #return make_response({"message": 'success', "data" : data}, HTTP_200_OK)
        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class allMoviesByuser(Resource):
    
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        data = models.userFetch.allMoviesByUser(user["userid"])
        #return make_response({"message": 'success', "data" : data}, HTTP_200_OK)
        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class singleMovie(Resource):
    
    def get(self, id):

        data = models.userFetch.singleMovie(id)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_400_BAD_REQUEST)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class moviesByGenre(Resource):
    
    def get(self, name):

        req = reqparse.RequestParser()
        req.add_argument('sort', help="sort")
        args = req.parse_args()

        if args['sort']:
            sort = args['sort']
        else:
            sort = 'DESC'

        data = models.userFetch.moviesByGenre(name, str(sort))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class moviesByGenreByUser(Resource):

    @jwt_required()
    def get(self, name):

        user = get_jwt_identity()
        req = reqparse.RequestParser()
        req.add_argument('sort', help="sort")
        args = req.parse_args()

        if args['sort']:
            sort = args['sort']
        else:
            sort = 'DESC'

        data = models.userFetch.moviesByGenreByUser(user["userid"], name, str(sort))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class getGenre(Resource):
    
    def get(self, name):

        data = models.userFetch.getGenre(name)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class getGenres(Resource):
    
    def get(self):

        data = models.userFetch.getGenres()
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class search(Resource):
    
    def get(self, search):

        data = models.userFetch.search(search)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)
class searchByUser(Resource):

    @jwt_required()
    def get(self, search):

        user = get_jwt_identity()
        data = models.userFetch.searchByUser(user["userid"], search)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class mylist(Resource):

    @jwt_required()
    def get(self):
        user = get_jwt_identity()

        data = models.userFetch.Mylist(int(user["userid"]))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

    @jwt_required()
    def post(self):
        user = get_jwt_identity()

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('movieid', help="Movieid is required", required=True)
        args = req.parse_args()

        if not models.userFetch.checkMylist(int(user["userid"]), int(args['movieid'])):
            if models.userFetch.addMylist(int(user["userid"]), int(args['movieid'])):
                return make_response({"message": "success", "action": "post"}, HTTP_200_OK)
            return make_response({"message": "failed"}, HTTP_400_BAD_REQUEST)
        else:
            if models.userFetch.delMylistBMId(int(user["userid"]), int(args['movieid'])):
                return make_response({"message": "success", "action": "delete"}, HTTP_200_OK)
            return make_response({"message": "failed"}, HTTP_400_BAD_REQUEST)
            

    @jwt_required()
    def delete(self):
        user = get_jwt_identity()

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('mylistid', help="mylistid is required", required=True)
        args = req.parse_args()

        if models.userFetch.delMylist(int(user["userid"]), int(args['mylistid'])):
            return make_response({"message": "success"}, HTTP_200_OK)
        return make_response({"message": "failed"}, HTTP_400_BAD_REQUEST)

class contactus(Resource):

    def post(self):

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('name', help="Fullname is required", required=True)
        req.add_argument('email', help="Email is required", required=True)
        req.add_argument('phonenumber', help="phonenumber is required", required=True)
        req.add_argument('message', help="message is required", required=True)
        args = req.parse_args()

        if args['name'].strip() == '' or args['email'].strip() == '' or args['phonenumber'].strip() == '' or args['message'].strip() == '':
            abort(HTTP_400_BAD_REQUEST, message="fill all inputs")

        if not models.EmailValidate(args['email']):
            abort(HTTP_400_BAD_REQUEST, message="Email is not valid")      

        if models.userFetch.addcontactus(**args):
            return make_response({"message": "success"}, HTTP_200_OK)


class vdQuality(Resource):
    
    @jwt_required()
    def get(self, movieId):
        user = get_jwt_identity()
        movieIid = movieId

        data = models.userFetch.vdQuality(movieIid, user["userid"])
        if not data:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class toPay(Resource):
    
    @jwt_required()
    def get(self, movieCvId):
        user = get_jwt_identity()
        movieCvId = movieCvId


        data = models.userFetch.toPay(movieCvId, user["userid"])
        if not data:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class payment(Resource):

    def post(self):
        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('userId', help="userId is required", required=True)
        req.add_argument('movieId', help="movieId is required", required=True)
        req.add_argument('mvCvId', help="mvCvId is required", required=True)
        req.add_argument('price', help="price is required", required=True)

        args = req.parse_args()

        data = models.userFetch.payment(**args)
        if not data:
            return make_response({"message": "Failed"}, HTTP_400_BAD_REQUEST)

        return make_response({"message": "success"}, HTTP_200_OK)
        

class getAvailableForMv(Resource):

    @jwt_required()
    def get(self, movieId):

        user = get_jwt_identity()
        data = models.userFetch.getAvailableForMv(movieId, user["userid"])
        if not data:
            return make_response({"message": "No quality founded"}, HTTP_400_BAD_REQUEST)
        else:
            return make_response({"message": "success","data" : data}, HTTP_200_OK)

class genresWithMovies(Resource):
    
    def get(self):

        req = reqparse.RequestParser()
        req.add_argument('sort', help="sort")
        args = req.parse_args()

        if args['sort']:
            sort = args['sort']
        else:
            sort = 'DESC'

        data = models.userFetch.allGenresWMv(str(sort))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class genresWithMoviesByUser(Resource):

    @jwt_required()
    def get(self):

        user = get_jwt_identity()
        req = reqparse.RequestParser()
        req.add_argument('sort', help="sort")
        args = req.parse_args()

        if args['sort']:
            sort = args['sort']
        else:
            sort = 'DESC'

        data = models.userFetch.allGenresWMvByUser(user["userid"], str(sort))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)


class mylistcheck(Resource):

    @jwt_required()
    def post(self):
        user = get_jwt_identity()

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('movieid', help="Movieid is required", required=True)
        args = req.parse_args()

        if models.userFetch.checkMylist(int(user["userid"]), int(args['movieid'])):
            return make_response({"message": True}, HTTP_200_OK)
        return make_response({"message": False}, HTTP_404_NOT_FOUND)
        
class userNotif(Resource):

    @jwt_required()
    def get(self):

        user = get_jwt_identity()

        data = models.userFetch.userGetNots(int(user['userid']))

        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)
    
    @jwt_required()    
    def post(self):

        user = get_jwt_identity()

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('type', help="type is required", required=True)
        req.add_argument('linkId', help="linkId is required")
        req.add_argument('description', help="PhoneNumber is required")

        args = req.parse_args()

        ''' if args['description'] == None:
            args['description'] = ''

        if args['linkId'] == None:
            args['linkId'] = '' '''


        if not models.userFetch.AdduserNotif(int(user['userid']), **args):
            return make_response({"message": "Failed"}, HTTP_400_BAD_REQUEST)

        return make_response({"message": "success"}, HTTP_200_OK)

    




""" Short movie """


class allsMovies(Resource):
    
    def get(self):

        data = models.userFetch.allsMovies()
        #return make_response({"message": 'success', "data" : data}, HTTP_200_OK)
        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class singlesMovie(Resource):
    
    def get(self, id):

        data = models.userFetch.singlesMovie(id)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_400_BAD_REQUEST)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class smoviesByGenre(Resource):
    
    def get(self, name):

        req = reqparse.RequestParser()
        req.add_argument('sort', help="sort")
        args = req.parse_args()

        if args['sort']:
            sort = args['sort']
        else:
            sort = 'DESC'

        data = models.userFetch.smoviesByGenre(name, str(sort))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class genresWithsMovies(Resource):
    
    def get(self):

        req = reqparse.RequestParser()
        req.add_argument('sort', help="sort")
        args = req.parse_args()

        if args['sort']:
            sort = args['sort']
        else:
            sort = 'DESC'

        data = models.userFetch.allGenresWsMv(str(sort))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)


""" end """


''' Otherentvd '''

class behindscenes(Resource):
    
    def get(self):

        data = models.userFetch.getBehindScenes()
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class behindscene(Resource):

    def get(self, id):

        data = models.userFetch.getBehindScene(id)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class documentaries(Resource):
    
    def get(self):

        data = models.userFetch.documentaries()
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class documentary(Resource):
    
    def get(self, id):

        data = models.userFetch.documentary(id)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class searchBehindScene(Resource):
    
    def get(self, search):

        data = models.userFetch.searchBehindScene(search)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

class searchDocumentary(Resource):

    def get(self, search):

        data = models.userFetch.searchDocumentary(search)
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_404_NOT_FOUND)

        return make_response({"message": "success","data" :data}, HTTP_200_OK)

''' end '''


api.add_resource(homeSlides, '/homeslides')
api.add_resource(allMovies, '/movies')
api.add_resource(allMoviesByuser, '/moviesbyuser')
api.add_resource(singleMovie, '/movie/<string:id>')
api.add_resource(getGenres, '/genres')
api.add_resource(getGenre, '/genre/<string:name>')
api.add_resource(moviesByGenre, '/moviesbygenre/<string:name>')
api.add_resource(moviesByGenreByUser, '/moviesbygenrebyuser/<string:name>')
api.add_resource(search, '/search/<string:search>')
api.add_resource(searchByUser, '/searchbyuser/<string:search>')
api.add_resource(mylist, '/mylist')
api.add_resource(mylistcheck, '/mylistcheck')
api.add_resource(contactus, '/contactus')
api.add_resource(vdQuality, '/videoquality/<string:movieId>')
api.add_resource(toPay, '/topay/<string:movieCvId>')
api.add_resource(payment, '/payment')
api.add_resource(getAvailableForMv, '/getmovievideosrc/<string:movieId>')
api.add_resource(genresWithMovies, '/genresWithMovies')
api.add_resource(genresWithMoviesByUser, '/genresWithMoviesbyuser')
api.add_resource(userNotif, '/notification')


#short movie
api.add_resource(allsMovies, '/smovies')
api.add_resource(singlesMovie, '/smovie/<string:id>')
api.add_resource(smoviesByGenre, '/smoviesbygenre/<string:name>')
api.add_resource(genresWithsMovies, '/genresWithsMovies')


#otherentvd

api.add_resource(behindscenes, '/behindscene')
api.add_resource(behindscene, '/behindscene/<string:id>')
api.add_resource(documentaries, '/documentaries')
api.add_resource(documentary, '/documentary/<string:id>')
api.add_resource(searchDocumentary, '/searchDocumentary/<string:search>')
api.add_resource(searchBehindScene, '/searchBehindScene/<string:search>')
