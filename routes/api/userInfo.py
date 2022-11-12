from flask_mail import Message
from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
import models
from constants.http_status_codes import *
from models.encordec.cryword import wordDec
from .userAuth import api
import phonenumbers
import werkzeug

class userInfo(Resource):

    @jwt_required()
    def get(self):
        user = get_jwt_identity()

        data = models.userinfo.allUserDet(int(user["userid"]))
        if len(data) == 0:
            return make_response({"message": "Not found", "data" :data}, HTTP_401_UNAUTHORIZED)
 
        return make_response({"message": "success","data" :data}, HTTP_200_OK)

    @jwt_required()
    def patch(self):
        
        user = get_jwt_identity()

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('firstName', help="firstName is required", required=True)
        req.add_argument('lastName', help="lastName is required", required=True)
        req.add_argument('username', help="username is required", required=True)
        req.add_argument('PhoneNumber', help="PhoneNumber is required", required=True)
        req.add_argument('profile', help="profile is required", required=True)
        req.add_argument('password', help="password is required", required=True)

        args = req.parse_args()


        if args['firstName'].strip() == '' or args['lastName'].strip() == '' or args['username'].strip() == '' or args['PhoneNumber'].strip() == '' or args['profile'].strip() == '' or args['password'].strip() == '':
            return make_response({"message": "Fill all inputs", 'type': 'error'}, HTTP_400_BAD_REQUEST)
        
        if models.userAuth.userCheckUsernameItSelf(user["userid"] ,args['username']):
            return make_response({"message": "Username is taken", 'type': 'error'}, HTTP_409_CONFLICT)

        try:
            phnValid = phonenumbers.is_valid_number(phonenumbers.parse(str(args['PhoneNumber'])))
        except:
            phnValid = False

        if not phnValid:
            return make_response({"message": "Phone number is invalid (it must contains your country code ex: +25078947234)", 'type': 'error'}, HTTP_400_BAD_REQUEST)

        if not models.userinfo.CheckUserPassw(user["userid"], args["password"]):
            return make_response({"message": "Password are not match", 'type': 'error'}, HTTP_400_BAD_REQUEST)


        if not models.userinfo.updateuserInfo(user["userid"], **args):
            return make_response({"message": "Failed to update", 'type': 'error'}, HTTP_400_BAD_REQUEST)
        return make_response({"message": "Updated", 'type': 'success'}, HTTP_200_OK)


class userChangePassw(Resource):

    @jwt_required()
    def patch(self):

        user = get_jwt_identity()

        req = reqparse.RequestParser(bundle_errors=True)
        req.add_argument('currentPassw', help="currentPassw is required", required=True)
        req.add_argument('newPassw', help="newPassw is required", required=True)
        req.add_argument('confirmPassw', help="confirmPassw is required", required=True)

        args = req.parse_args()


        if args['newPassw'].strip() == '' or args['confirmPassw'].strip() == '' or args['currentPassw'].strip() == '':
            return make_response({"message": "Fill all inputs", 'type': 'error'}, HTTP_400_BAD_REQUEST)

        if not models.userinfo.CheckUserPassw(user["userid"], args["currentPassw"]):
            return make_response({"message": "Unknown password", 'type': 'error'}, HTTP_400_BAD_REQUEST)
        
        if not models.passwordValidate(str(args["newPassw"])):
            return make_response({"message": "Password must be atleast 6 characters and contains uppercase, lowercase, number and symbols", 'type': 'error'}, HTTP_400_BAD_REQUEST)

        if str(args["newPassw"]) != str(args["confirmPassw"]):
            return make_response({"message": "Passwords are not equal", 'type': 'error'}, HTTP_400_BAD_REQUEST)

        if models.userAuth.changeUserPassw(user["userid"], args["newPassw"]):
            return make_response({"message": "success", 'type': 'success'}, HTTP_200_OK)
        else:
            return make_response({"message": "Fail to change password", 'type': 'error'}, HTTP_400_BAD_REQUEST)

class validtoken(Resource):

    @jwt_required()
    def get(self):

        return make_response({"message": "valid token"}, HTTP_200_OK)


api.add_resource(validtoken, '/validtoken')
api.add_resource(userInfo, '/userinfo')
api.add_resource(userChangePassw, '/changepassword')