from flask_restful import Resource


class Intro(Resource):
    def get(self):
        return {"ROUTES":
            [{
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
                "Endpoint":"/admin/id",
                "Description":"Get admin id",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/admin/all",
                "Description":"Get list of all admins",
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
                "Endpoint":"/admin/registration",
                "Description":"Get all registrations of the admin that requests.",
                "Header":"jwt_token",
                "Method":"GET"
            },
            {
                "Endpoint":"/admin/registration",
                "Description":"Register for an event.",
                "form-data":{
                    "name":"name",
                    "email":"email",
                    "mobile_number":"mobile_number",
                    "image":"image",
                    "type":"type",
                    "no_of_tickets":"no_of_tickets",
                    "event_name":"event_name"
                },
                "Method":"POST"
            },
            {
                "Endpoint":"/event",
                "Description":"get events for the admin",
                "Method":"GET",
                "Header":"jwt_token",
            },
            {
                "Endpoint":"/event",
                "Description":"create new event for the admin",
                "Body":{"event_name":"event_name"},
                "Header":"jwt_token",
                "Method":"Post"
            },
            {
                "Endpoint":"/event",
                "Description":"Delete event for the admin",
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
                "Endpoint":"/event/count",
                "Description":"get events registration count for the admin",
                "Method":"GET",
                "Header":"jwt_token",
            },
            {
            "Endpoint":"/contact",
            "Description":"Contact us",
            "Body":{"name":"Firstname Lastname",
                    "email":"someone@something.com",
                    "message":"Your message"},
            "Method":"Post"
            },
            {
            "Endpoint":"/contact",
            "Description":"Contact us",
            "Header":"jwt_token",
            "Method":"GET"
            },
            {
            "Endpoint":"/contact",
            "Description":"Contact us",
            "Body":{"name":"Firstname Lastname",
                    "email":"someone@something.com",
                    "message":"Your message"},
            "Header":"jwt_token",
            "Method":"Delete"
            },
        ]}, 200
