import os
from configparser import ConfigParser
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.admin_resource import (AdminLogin,
                                      AdminLogout,
                                      AdminRegister,
                                      AdminChangePwd,
                                      GetUser)
from resources.registration_resource import (Registration,
                                             RegistrationById,
                                             RegistrationType)
from resources.documentation import Intro
from resources.events_resource import Events, EventList
from blacklist import BLACKLIST

parser = ConfigParser()
parser.read('config.ini')

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY']=parser.get('APP', 'SECRET_KEY')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims(identity):
    if identity['username'] == parser.get('APP', 'ADMIN_NAME'):
        return {'is_admin':True}
    return {'is_admin':False}


@jwt.token_in_blacklist_loader
def check_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_error_message():
    return {
            "message":"Token has expired.",
            "error_code":"expired_token"
    },401


@jwt.invalid_token_loader
def invalid_error_message(error):
    return{
        "message":"Invalid Token.",
        "error_code":"invalid_token"
    },401


@jwt.unauthorized_loader
def missing_header_message(error):
    return{
        "message":"JWT not found in request.",
        "error_code":"missing_jwt"
    },401


@jwt.revoked_token_loader
def revoked_error_message():
    return{
        "message":"Login Again to access.",
        "error_code":"token_revoked"
    },401


api=Api(app)
api.add_resource(Intro,'/')
api.add_resource(AdminRegister,'/admin/register')
api.add_resource(AdminLogin,'/admin/login')
api.add_resource(AdminLogout,'/admin/logout')
api.add_resource(AdminChangePwd,'/admin/changepwd')
api.add_resource(GetUser,'/admin/getuser')
api.add_resource(RegistrationById,'/admin/registrationid/<string:registration_id>')
api.add_resource(Registration,'/admin/registration/all')
api.add_resource(RegistrationType,'/admin/registration/type/<string:event_name>')
api.add_resource(Events,'/event')
api.add_resource(EventList,'/event/all')
#api.add_resource(ContactAdmin,'/contact')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
