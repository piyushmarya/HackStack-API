# Error and Success Message handling.

# Importing all required modules.
from datetime import datetime

class Codes:
    def __init__(self, message, code, solution=None):
        self.message = message
        self.code = code
        self.solution = solution

    def to_json(self):
        if "E" in self.code:
            return {
                "message":self.message,
                "code":self.code,
                "solution":self.solution,
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "status": "Interrupted"
            }
        else:
            return {
                "message":self.message,
                "code":self.code,
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "status": "Success"
            }


# Creating objects for each message.
INVALID_CREDENTIALS_ERROR = Codes("The entered credentials are invalid.", "E3", "Enter the correct credentials and try again")
REGISTER_ADMIN_ERROR = Codes("Administrator not registered", "E2", "Register admin before trying again.")
INSUFFICIENT_PRIVELEGES_ERROR = Codes("You dont have the adequate priveleges for this operation", "E1", "Contact us to get priveleges.")
ADMIN_EXISTS_ERROR = Codes("The Admin name entered already exists", "E4", "Change the Admin name and try again.")
NO_ADMIN_ERROR = Codes("No Admins exists", "E5", "Register administrator before trying again.")
REGISTRATION_ERROR = Codes("An error occured while registering.", "E6", "Internal server error, Try again later.")
UNKNOWN_ERROR = Codes("Unknown error occured", "E7", "Internal server error, try again later.")
CHANGE_PASSWORD_ERROR = Codes("Unable to change password.", "E8", "Internal server error, try again later.")
INCORRECT_OLD_PASSWORD_ERROR = Codes("The old password you entered is incorrect", "E9", "Enter the correct old password.")
NO_REGISTRATIONS_ERROR = Codes("No registrations found", "E10","No one has yet joined your event.")
REGISTRATION_EXISTS_ERROR = Codes("Registration with same email already exists.", "E11", "You have registred with this email once.")
NO_EVENT_ERROR = Codes("No events found", "E12", "Create an event.")
EVENT_ADD_ERROR = Codes("Unable to add event, try again later", "E13", "Internal server error, try again later.")
EVENT_DELETE_ERROR = Codes("Unable to delete event, try again later", "E14", "Internal server error, try again later.")
ONGOING_EVENT_ERROR = Codes("Ongoing Event", "E15", "Change event name and try again.")
EXPIRED_TOKEN_ERROR = Codes("The token has expired.", "E16", "Create a new token and try again.")
INVALID_TOKEN_ERROR = Codes("The token is invalid.", "E17", "Send in the correct token")
MISSING_TOKEN_ERROR = Codes("The token missing in the header.", "E18", "Make a request with the token in the header.")
REVOKED_TOKEN_ERROR = Codes("The token is revoked", "E19", "Create a new token and try again.")
MESSAGE_SEND_ERROR = Codes("Unable to send message,try again later", "E20", "Internal server error, try again later.")
MESSAGE_DELETE_ERROR = Codes("Unable to delete message,try again later", "E21", "Internal server error, try again later.")
MESSAGE_LOAD_ERROR = Codes("Unable to load messages,try again later", "E22", "Internal server error, try again later.")
PASSWORD_CHANGED = Codes("Password successfully changed","S2")
ADMIN_CREATED = Codes("New admin successfully created, Login to access more features","S1")
ADMIN_DELETED = Codes("Admin successfully deleted", "S3")
EVENT_ADDED =Codes("New event added successfully", "S4")
EVENT_DELETED = Codes("Event deleted successfully", "S5")
LOGOUT = Codes("Logout Successful", "S6")
MESSAGE_SENT = Codes("Your message is sent, we'll get in touch soon", "S7")
MESSAGE_DELETED = Codes("Message is deleted", "S8")
