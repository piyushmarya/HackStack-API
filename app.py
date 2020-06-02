# Creates an API.

# Importing all required libraries.
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Importing all required modules.
from resources.admin_resource import (AdminLogin,
                                      AdminLogout,
                                      AdminRegister,
                                      AdminChangePwd,
                                      GetAdminId,
                                      GetAllAdmins,
                                      DeleteAdmin)
from resources.event_registration_resource import (EventRegistration,
                                                   EventRegistrationByNumber)
from resources.events_resource import Events, EventList, EventRegistrationCount
from resources.documentation import Intro
from resources.contact_resource import ContactAdmin
from utils.status import (INVALID_TOKEN_ERROR,
                         EXPIRED_TOKEN_ERROR,
                         REVOKED_TOKEN_ERROR,
                         MISSING_TOKEN_ERROR)
from utils.blacklist import BLACKLIST
from utils.config_parser import parser

# Initialize Flask app
app = Flask(__name__)

# Enabling Cross-origin resource sharing on all routes
CORS(app)

# Setting up all required configurations
app.config['SECRET_KEY']=parser.get('API', 'SECRET_KEY')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(parser.get('API', 'EXPIRE_TIME'))
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Following function return custom error messages for jwt related errors.

@jwt.user_claims_loader
def add_claims(identity):
    """
    Adds an extra claim to token if the super admin logs in.
    """
    if identity['username'] == parser.get('API', 'ADMIN_NAME'):
        return {'is_super_admin':True}
    return {'is_super_admin':False}


@jwt.token_in_blacklist_loader
def check_blacklist(decrypted_token):
    """
    Checks whether the recieved token has been blacklisted from being used.
    further.
    """
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_error_message():
    """
    Returns custom message if the jwt token recieved is expired.
    """
    return EXPIRED_TOKEN_ERROR.to_json(), 401


@jwt.invalid_token_loader
def invalid_error_message(error):
    """
    Returns custom message if the jwt token recieved is invalid.
    """
    return INVALID_TOKEN_ERROR.to_json(), 401


@jwt.unauthorized_loader
def missing_header_message(error):
    """
    Returns custom message if the jwt token is missing in the request.
    """
    return MISSING_TOKEN_ERROR.to_json(), 401


@jwt.revoked_token_loader
def revoked_error_message():
    """
    Returns custom message if the jwt token has been revoked.
    """
    return REVOKED_TOKEN_ERROR.to_json(), 401


# Flask-Restful initialization to enable resourceful routing.
api=Api(app)

# Adding all routes for the api
api.add_resource(Intro,'/')
api.add_resource(AdminRegister, '/admin/register')
api.add_resource(AdminLogin, '/admin/login')
api.add_resource(AdminLogout, '/admin/logout')
api.add_resource(AdminChangePwd, '/admin/changepwd')
api.add_resource(DeleteAdmin, '/admin/remove')
api.add_resource(GetAdminId, '/admin/id')
api.add_resource(GetAllAdmins, '/admin/all')
api.add_resource(EventRegistrationByNumber, '/admin/registrationid/<string:registration_number>')
api.add_resource(EventRegistration, '/registration')
api.add_resource(EventRegistrationCount, '/event/count')
api.add_resource(Events, '/event')
api.add_resource(EventList, '/event/all')
api.add_resource(ContactAdmin, '/contact')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
