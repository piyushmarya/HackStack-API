from datetime import datetime

class Codes:
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def to_json(self):
        return {
            "message":self.message,
            "code":self.code,
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "Interrupted" if "E" in self.code else "Success"
        }


INVALID_CREDENTIALS_ERROR = Codes("The entered credentials are invalid,Try again", "E3")
REGISTER_USER_ERROR = Codes("Register user first before trying again", "E2")
INSUFFICIENT_PRIVELEGES_ERROR = Codes("You dont have the adequate priveleges for this operation", "E1")
USER_EXISTS_ERROR = Codes("The username entered already exists", "E4")
REGISTRATION_ERROR = Codes("An error occured while registering, try again later", "E5")
UNKNOWN_ERROR = Codes("Unknown error occured", "E6")
CHANGE_PASSWORD_ERROR = Codes("Unable to change password, try again", "E7")
INCORRECT_OLD_PASSWORD_ERROR = Codes("The old password you entered is incorrect", "E8")
NO_REGISTRATIONS_ERROR = Codes("No registrations found", "E9")
NO_EVENT_ERROR = Codes("No events found", "E10")
EVENT_ADD_ERROR = Codes("Unable to add event, try again later", "E11")
EVENT_DELETE_ERROR = Codes("Unable to add event, try again later", "E12")
ONGOING_EVENT_ERROR = Codes("It is an ongoing event, change your event name", "E13")
EXPIRED_TOKEN_ERROR = Codes("The token has expired, create a new token and try again.", "E14")
INVALID_TOKEN_ERROR = Codes("The token is invalid, send in the correct token", "E15")
MISSING_TOKEN_ERROR = Codes("The token missing in the header, make request with the token", "E16")
REVOKED_TOKEN_ERROR = Codes("The token is revoked, create a new one", "E17")
PASSWORD_CHANGED = Codes("Password successfully changed","S2")
USER_CREATED = Codes("New user successfully created","S1")
USER_DELETED = Codes("User successfully deleted", "S3")
EVENT_ADDED =Codes("New event added successfully", "S4")
EVENT_DELETED = Codes("Event deleted successfully", "S5")
LOGOUT = Codes("Logout Successful", "S6")
