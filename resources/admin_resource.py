from passlib.hash import sha256_crypt
from uuid import uuid4
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                jwt_optional,
                                get_raw_jwt,
                                get_jwt_claims)

from blacklist import BLACKLIST
from models.admin_model import AdminMethods

admin_parser = reqparse.RequestParser()
admin_parser.add_argument('username',
                    type=str,
                    help="Username is a required field",
                    required=True)
admin_parser.add_argument('password',
                    type=str,
                    help="Password is a required field",
                    required=True)


class AdminRegister(Resource):

    @jwt_required
    def post(self):
        """
        Registers a new adminstrator.
        Parameters: Username,Password
        Returns: JSON message describing the status of request
        """
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Super Admin privilege required.'}, 401
        data = admin_parser.parse_args()
        admin_data = AdminMethods.fetch_by_username(data['username'])
        if admin_data:
            return{"message":"Admin already exists"},400
        if admin_data is None:
            data['uuid']=str(uuid4())
            admin_obj = AdminMethods(**data)
            if admin_obj.save_to_db():
                return {"message":"User Registered"},201
            return {
                "message":"Unknown error occured while registring.Try Again"
                },501
        return {"message":"Unknown error occured.Try Again."},501


class AdminLogin(Resource):
    def post(self):
        """
        Logs in the adminstrator.
        Parameters: Username,Password
        Returns: JSON message describing the status of request
        """
        data = admin_parser.parse_args()
        admin = AdminMethods.fetch_by_username(data['username'])
        if admin is None:
            return{"message":"Register Admin first"},400
        if admin is False:
            return {"message":"Unknown error occured"},501
        if admin and sha256_crypt.verify(data["password"], admin["password"]):
            identity={"uuid":admin['uuid'],
                      "username":data['username']}
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            },200
        return {"message":"Invalid Credentials"},401


class AdminLogout(Resource):

    @jwt_required
    def get(self):
        """
        Logs out adminstrator.
        Parameters:
        Returns: JSON message describing the status of request
        """
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message":"Log Out Successful"},201


class AdminChangePwd(Resource):
    admin_changepwd_parser = reqparse.RequestParser()
    admin_changepwd_parser.add_argument('username',
                        type=str,
                        help="Username is a required field",
                        required=True)
    admin_changepwd_parser.add_argument('old_password',
                        type=str,
                        help="old password is a required field",
                        required=True)
    admin_changepwd_parser.add_argument('new_password',
                        type=str,
                        help="New password is a required field",
                        required=True)

    @jwt_required
    def post(self):
        """
        Changes password for the adminstrator.
        Parameters: Username,New password
        Returns: JSON message describing the status of request
        """

        data = self.admin_changepwd_parser.parse_args()
        admin = AdminMethods.fetch_by_username(data['username'])
        jwt_username = get_jwt_identity()['username']
        if admin is None:
            return{"message":"Register Admin first"},400
        if  admin['username'] != jwt_username:
            return {"message":"Unauthourized"},401
        if admin and sha256_crypt.verify(data["old_password"], admin["password"]):
            admin_obj = AdminMethods(data['username'], data['new_password'])
            if admin_obj.change_pwd():
                return {"message":"Password Changed."},201
            else:
                return {
                    "message":"Unknown error occured while changing password. Try again."
                    },501
        else:
            return {"message":"Old password is incorrect"},400
        return {"message":"Unknown error occured"},501


class GetUser(Resource):

    @jwt_required
    def get(self):
        """
        Returns the user id of adminstrator.
        Parameters:
        Returns: JSON message containing id
        """
        return {"id":get_jwt_identity()},201
