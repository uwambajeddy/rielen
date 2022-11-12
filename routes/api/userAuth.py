import re
from flask import Blueprint, jsonify, make_response
from flask_mail import Message
from flask_restful import Api, Resource, reqparse, abort
from flask_jwt_extended import jwt_required, JWTManager, create_access_token, get_jwt_identity, create_refresh_token
import models
import phonenumbers
from constants.http_status_codes import *
from models.encordec.cryword import wordDec, wordEnc
import routes
#from datetime import timedelta

""" from .usermv import * """

jwt = JWTManager()

apiBlueprint = Blueprint('api', __name__, url_prefix= '/api/v1')
api = Api(apiBlueprint)

class mv(Resource):
    @jwt_required()
    def get(self):
        return jsonify({"message": "movie", "user": get_jwt_identity()})

class login(Resource):

    def post(self):

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('logname', help="username or email of user is required", required=True)
        req.add_argument('password', help="password of user is required", required=True)

        args = req.parse_args()

        if args['logname'].strip() == '' or args['password'].strip() == '':
            abort(HTTP_400_BAD_REQUEST, message="fill all inputs")

        user = models.userAuth.login(**args)

        if not user:
            abort(HTTP_401_UNAUTHORIZED, message="Failed to login")
        else:
    
            if user["action"] == "activation":
                return jsonify({"message": "sent activation link", "data": {"userId": wordEnc(user['id']), "email": user['email']}})

            if user["action"] == "success":

                """ time = timedelta(minutes= 15)
                print(time) """
                token = create_access_token(identity={"userid": user['id'], "email": user['email']})
                refresh = create_refresh_token(identity={"userid": user['id'], "email": user['email']})
                return make_response({"message": "login successful", "access_token": token, "refresh_token": refresh, "token_type": "Bearer"}, HTTP_200_OK)
        



class register(Resource):

    def post(self):

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('firstname', help="Firstname of user is required", required=True)
        req.add_argument('lastname', help="Lastname of user is required", required=True)
        req.add_argument('email', help="Email of user is required", required=True)
        req.add_argument('username', help="Username of user is required", required=True)
        req.add_argument('gender', help="gender of user is required", required=True)
        req.add_argument('password', help="Password of user is required", required=True)
        req.add_argument('cpassword', help="Confirm password of user is required", required=True)
        req.add_argument('phonenumber', help="Phonenumber of user is required", required=True)
        
        args = req.parse_args()

        if models.userAuth.userCheckEmail(args['email']):
            abort(HTTP_409_CONFLICT, message= "Email is taken")

        if models.userAuth.userCheckUsername(args['username']):
            abort(HTTP_409_CONFLICT, message= "Username is taken")

        if args['firstname'].strip() == '' or args['lastname'].strip() == '' or args['email'].strip() == '' or args['username'].strip() == '' or args['gender'].strip() == '' or args['password'].strip() == '' or args['cpassword'].strip() == '' or args['phonenumber'].strip() == '':
            abort(HTTP_400_BAD_REQUEST, message="fill all inputs")

        if args['gender'] not in ('female', 'male'):
            abort(HTTP_400_BAD_REQUEST, message="unknown gender")

        try:
            phnValid = phonenumbers.is_valid_number(phonenumbers.parse(str(args['phonenumber'])))
        except:
            phnValid = False

        if not phnValid:
            abort(HTTP_400_BAD_REQUEST, message="Phone number is invalid (must contains your country code ex: +25078947234)")

                    
        if not models.passwordValidate(str(args["password"])):
            #abort(HTTP_400_BAD_REQUEST, message="password must be atleast 6 characters and contains uppercase, lowercase, number and symbols")
            abort(HTTP_400_BAD_REQUEST, message="password must be at least 6 characters")
        
        if not models.EmailValidate(args['email']):
            abort(HTTP_400_BAD_REQUEST, message="Email is not valid")

        if str(args["password"]) != str(args["cpassword"]):
            abort(HTTP_400_BAD_REQUEST, message="passwords are not equal")
        
        pr = models.userAuth.register(**args)
        if pr['result']:
            return make_response({"message": "succeful", "data": pr['data']}, HTTP_201_CREATED)
        else:
            abort(HTTP_400_BAD_REQUEST, message="registeration failed")


class getEmailChangePassw(Resource):

    def post(self):

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('email', help="Email of user is required", required=True)

        args = req.parse_args()

        if args['email'].strip() == '':
            abort(HTTP_400_BAD_REQUEST, message="fill email input")
        
        if not models.EmailValidate(args['email']):
            abort(HTTP_400_BAD_REQUEST, message="Email is not valid")
        
        if not models.userAuth.userCheckEmail(args['email']):
            abort(HTTP_404_NOT_FOUND, message= "Email is not founded")
        
        if models.userAuth.sendUserTokenResetPassw(args['email']):
            return jsonify({"message": "succeful"})
        else:
            abort(HTTP_400_BAD_REQUEST, message= "Failed")
    
class resetUserPassw(Resource):

    def post(self):

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('password', help="password of user is required", required=True)
        req.add_argument('cpassword', help="cpassword of user is required", required=True)
        req.add_argument('user', help="UserId of user is required", required=True)
        req.add_argument('token', help="token of user is required", required=True)

        args = req.parse_args()

        if args['password'].strip() == '' or args['cpassword'].strip() == '':
            abort(HTTP_400_BAD_REQUEST, message="fill all inputs")

        if not models.passwordValidate(str(args["password"])):
            abort(HTTP_400_BAD_REQUEST, message="password must be atleast 6 characters and contains uppercase, lowercase, number and symbols")

        if str(args["password"]) != str(args["cpassword"]):
            abort(HTTP_400_BAD_REQUEST, message="passwords are not equal")

        if models.userAuth.checkUserExpTokenRP(models.wordDec(str(args['user'])), str(args['token'])):
            if models.userAuth.changeUserPassw(models.wordDec(str(args['user'])), args["password"]):
                return jsonify({"message": "success"})
            else:
                abort(HTTP_400_BAD_REQUEST, message="fail to change password")
        else:
            abort(HTTP_400_BAD_REQUEST, message="Token is expired")


class activateUserByLink(Resource):
    
    def get(self, id):

        #decrypting get id
        rec = int(models.wordDec(id))

        #checking
        if not models.userAuth.ckeckingUserE(rec):
            abort(HTTP_400_BAD_REQUEST, message="User not exist")

        #activating user account
        if models.userAuth.activateUserById(rec):
            return jsonify({"message": "success"})
        else:
            abort(HTTP_400_BAD_REQUEST, message="Failed to activate your account")

class refreshToken(Resource):
    
    @jwt_required(refresh=True)
    def get(self):

        identity = get_jwt_identity()
        token = create_access_token(identity=identity)
        refresh = create_refresh_token(identity=identity)
        return make_response({"message": "refresh token", "access_token": token, "refresh_token": refresh, "token_type": "Bearer"}, HTTP_200_OK)

class resendActivationLinkToUser(Resource):
    
    def get(self, id):

        data = models.userAuth.resendActivationLink(int(wordDec(id)))

        if data['result']:
            return make_response({"message": "successful", "data": data['data']}, HTTP_200_OK)
        else:
            abort(HTTP_400_BAD_REQUEST, message="Failed to send activation link")



api.add_resource(login, '/login')
api.add_resource(refreshToken, '/refresh_token')
api.add_resource(register, '/register')
api.add_resource(mv, '/movie')
api.add_resource(getEmailChangePassw, '/sendresetpassw')
api.add_resource(resetUserPassw, '/resetUserPassw')
api.add_resource(activateUserByLink, '/activate/<string:id>')
api.add_resource(resendActivationLinkToUser, '/resendLink/<string:id>')

""" api.add_resource(homeSlides, '/homeslides') """