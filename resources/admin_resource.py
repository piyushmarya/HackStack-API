# Handles all required routes for administrator related functionality.

# Importing all required libraries
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

# Importing all the required modules
from models.admin_model import AdminMethods
from models.event_model import EventMethods
from models.event_registration_model import RegistrationMethods

from utils.blacklist import BLACKLIST
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
from utils.config_parser import parser

# A parser to validate the request body
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
    """Registers a new administrator"""
    def post(self):
        """
        Description: Registers a new adminstrator with the provided credentials.
        Returns: JSON message describing the status of request
        """
        # Parses the request body and stores in a dictionary.
        data = admin_parser.parse_args()
        # Check if the admin of the same username exists or not.
        admin_data = AdminMethods.fetch_by_username(data['username'])
        if admin_data:
            return ADMIN_EXISTS_ERROR.to_json(),400
        if admin_data is None:
            data['uuid']=str(uuid4()) #create a uuid for admin.
            admin_obj = AdminMethods(**data)
            if admin_obj.save_to_db():
                return ADMIN_CREATED.to_json(), 201
            return REGISTRATION_ERROR.to_json(),501
        return UNKNOWN_ERROR.to_json(), 501


class AdminLogin(Resource):
    def post(self):
        """
        Logs in the adminstrator.
        Returns: JSON message describing the status of request
        """
        # Parses the request body and stores it in a dictionary.
        data = admin_parser.parse_args()
        # check if the admin with the provides username exists or not.
        admin_details = AdminMethods.fetch_by_username(data['username'])
        if admin_details is None:
            return REGISTER_ADMIN_ERROR.to_json(), 400
        if admin_details is False:
            return UNKNOWN_ERROR.to_json(), 501

        # Verify if admin exists and the pasword is correct.
        if admin_details and sha256_crypt.verify(data["password"], admin_details["password"]):
            # Create an identity for the user that will be stored in the jwt token
            identity={"uuid":admin_details['uuid'],
                      "username":data['username']}
            # JWT access and refresh token creation using the above created identity.
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token,
                "admin_name":data['username'],
                "expires_in":int(parser.get('API', 'EXPIRE_TIME')),
                "registered_user":True
            },200

        return INVALID_CREDENTIALS_ERROR.to_json(), 400


class AdminLogout(Resource):

    @jwt_required
    def get(self):
        """
        Logs out adminstrator.
        Returns: JSON message describing the status of request
        """
        # Get the JWT token identifier(JTI)
        jti = get_raw_jwt()['jti']
        # Add the jti to blacklist and prevent from being used further.
        BLACKLIST.add(jti)
        return LOGOUT.to_json(), 201


class AdminChangePwd(Resource):
    """Changes Password for the admin"""

    # parser to validate and parse request body.
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
        # Parse the request body and stores in a dictionary.
        data = self.admin_changepwd_parser.parse_args()
        admin_details = AdminMethods.fetch_by_username(data['username'])
        # Get the username from identity of the jwt token.
        jwt_username = get_jwt_identity()['username']
        if admin_details is None:
            return REGISTER_ADMIN_ERROR.to_json(),400
        # Check if the username in the jwt token and the username in the request
        # body is the same.
        if  admin_details['username'] != jwt_username:
            return INSUFFICIENT_PRIVELEGES_ERROR.to_json(),403

        # Verify if admin exists and the old password is correct.
        if admin_details and sha256_crypt.verify(data["old_password"], admin_details["password"]):
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
        # Get the claims in jwt token.
        claims = get_jwt_claims()
        # Return different dicts for super admin and admin
        if claims["is_super_admin"]:
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
        # Get the claims from the jwt token.
        claims = get_jwt_claims()
        if claims['is_super_admin']:
            # Fetch all the admins in a list.
            all_admins = AdminMethods.get_all_admins()
            if all_admins:
                return all_admins, 200
            try:
                if not len(all_admins):
                    return NO_ADMIN_ERROR.to_json(), 400
            except TypeError:
                return UNKNOWN_ERROR.to_json(), 501
        return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 401


class DeleteAdmin(Resource):
    delete_admin_parser = reqparse.RequestParser()
    delete_admin_parser.add_argument('username',
                        type=str,
                        help="Username is a required field",
                        required=True)

    @jwt_required
    def delete(self):
        """
        Deletes an admin and all its corresponding information.
        Parameters:None
        Returns:JSON message describing the status of request
        """
        # Parses the request body and stores in a dictionary.
        data = self.delete_admin_parser.parse_args()
        # Check if the username provided is not that of the super admin.
        if data['username'] == parser.get('API','ADMIN_NAME'):
            return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 401
        # Get the claims from jwt_token
        claims = get_jwt_claims()

        # Check if the username in the jwt token and the username in the request
        # body is the same if the request has not been made by the super admin.
        if not claims["is_super_admin"]:
            id = get_jwt_identity()
            jwt_username = id['username']
            if jwt_username != data['username']:
                return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 401
        # Fetch all the events the admin has created.
        event_details = EventMethods.get_events(data["username"])
        if event_details:
            event_name_list = [i['event_name'] for i in event_details]
            event_obj = EventMethods(event_name_list, data["username"])

            # Delete all the admin events and the registrations for the event.
            if event_obj.delete_from_db() and RegistrationMethods.delete_event_registrations(event_name_list):
                # Delete the user only if the all the corresponding details are deleted.
                if AdminMethods.delete_admin(data["username"]):
                    return ADMIN_DELETED.to_json(), 200
            else:
                return UNKNOWN_ERROR.to_json(), 501

        # If the admin has no events.
        else:
            if AdminMethods.fetch_by_username(data["username"]):
                if AdminMethods.delete_admin(data["username"]):
                    return ADMIN_DELETED.to_json(), 200
                return UNKNOWN_ERROR.to_json(), 501
            else:
                return NO_ADMIN_ERROR.to_json(), 400
        return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 401
