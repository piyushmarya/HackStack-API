from flask_restful import Resource


class Intro(Resource):
    def get(self):
        return [
            {
                "Endpoint":"/admin/register",
                "Description":"Registor a new admin",
                "Body":{"username":"username",
                        "password":"password"},
                "Method":"POST"
            },
            {
                "Endpoint":"/admin/login",
                "Description":"Login admin",
                "Body":{"username":"username",
                        "password":"password"},
                "Method":"POST"
            },
            {
                "Endpoint":"/admin/logout",
                "Description":"Logout Admin",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/admin/changepwd",
                "Description":"Change admin password",
                "Body":{"username":"username",
                        "new_password":"new password",
                        "old_password":"old password"},
                "Header":"jwt_token",
                "Method":"POST"
            },
            {
                "Endpoint":"/admin/get_user",
                "Description":"Get user id",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/admin/registrationid/<string:registration_id>",
                "Description":"Get user details from registration id",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/admin/registration/all",
                "Description":"Get all registrations",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/admin/registration/type",
                "Description":"Get count of registration types",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/event",
                "Description":"get events for the user",
                "Method":"GET",
                "Header":"jwt_token",
            },
            {
                "Endpoint":"/event",
                "Description":"Add events for the user",
                "Body":{"event_name":"event_name"},
                "Header":"jwt_token",
                "Method":"Post"
            },
            {
                "Endpoint":"/event",
                "Description":"Add events for the user",
                "Body":{"event_name":"event_name"},
                "Header":"jwt_token",
                "Method":"Delete"
            },
            {
                "Endpoint":"/event/all",
                "Description":"get all events",
                "Method":"GET"
            },
            {
            "Endpoint":"/contact",
            "Description":"Contact us",
            "Body":{"name":"Firstname Lastname",
                    "email":"someone@something.com",
                    "message":"Your message"},
            "Method":"Post"
            }
        ]
