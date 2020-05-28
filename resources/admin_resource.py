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

from utils.blacklist import BLACKLIST
from models.admin_model import AdminMethods
from utils.status import (INVALID_CREDENTIALS_ERROR,
                          REGISTER_ADMIN_ERROR,
                          INSUFFICIENT_PRIVELEGES_ERROR,
                          ADMIN_EXISTS_ERROR,
                          REGISTRATION_ERROR,
                          UNKNOWN_ERROR,
                          CHANGE_PASSWORD_ERROR,
                          INCORRECT_OLD_PASSWORD_ERROR,
                          NO_ADMIN_ERROR,
                          ADMIN_CREATED,
                          ADMIN_DELETED,
                          LOGOUT,
                          PASSWORD_CHANGED)

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
            return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 403
        data = admin_parser.parse_args()
        admin_data = AdminMethods.fetch_by_username(data['username'])
        if admin_data:
            return ADMIN_EXISTS_ERROR.to_json(),400
        if admin_data is None:
            data['uuid']=str(uuid4())
            admin_obj = AdminMethods(**data)
            if admin_obj.save_to_db():
                return ADMIN_CREATED.to_json(), 201
            return REGISTRATION_ERROR.to_json(),501
        return UNKNOWN_ERROR.to_json(), 501


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
            return REGISTER_ADMIN_ERROR.to_json(), 400
        if admin is False:
            return UNKNOWN_ERROR.to_json(), 501
        if admin and sha256_crypt.verify(data["password"], admin["password"]):
            identity={"uuid":admin['uuid'],
                      "username":data['username']}
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token,
                "admin_name":data['username'],
                "expires_in":3600,
                "registered_user":True   
            },200
        return INVALID_CREDENTIALS_ERROR.to_json(), 400


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
        return LOGOUT.to_json(), 201


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
            return REGISTER_ADMIN_ERROR.to_json(),400
        if  admin['username'] != jwt_username:
            return INSUFFICIENT_PRIVELEGES_ERROR.to_json(),403
        if admin and sha256_crypt.verify(data["old_password"], admin["password"]):
            admin_obj = AdminMethods(data['username'], data['new_password'])
            if admin_obj.change_pwd():
                return PASSWORD_CHANGED.to_json(), 201
            else:
                return CHANGE_PASSWORD_ERROR.to_json(), 501
        else:
            return INCORRECT_OLD_PASSWORD_ERROR.to_json(),400
        return UNKNOWN_ERROR.to_json(),501


class GetAdminId(Resource):

    @jwt_required
    def get(self):
        """
        Returns the user id of adminstrator.
        Parameters:
        Returns: JSON message containing id
        """
        claims = get_jwt_claims()
        if claims["is_admin"]:
            return {"id":get_jwt_identity(),"is_admin":True}, 201
        return {"id":get_jwt_identity()},201


class GetAllAdmins(Resource):

    @jwt_required
    def get(self):
        """
        Returns names and uuid of all admins.
        Parameters:
        Return:List of admins
        """
        claims = get_jwt_claims()
        if claims['is_admin']:
            all_admins = AdminMethods.get_all_admins()
            if all_admins:
                return all_admins, 200
            try:
                if not len(all_admins):
                    return NO_ADMIN_ERROR.to_json(), 400
            except TypeError:
                return UNKNOWN_ERROR.to_json(), 501
        return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 401
