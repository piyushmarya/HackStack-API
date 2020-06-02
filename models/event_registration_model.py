
# Importing all required libraries
import json
from pymongo import errors
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from werkzeug.utils import secure_filename

# Importing all the required modules.
from utils.db import db
from utils.config_parser import parser

class RegistrationMethods:
    registration_collection=db.registration_details

    def __init__(self, name, email, mobile_number, image, type, no_of_tickets,
                 event_name, registration_number):
        self.name = name # Name of the person that registered.
        self.email = email # Email of the person that registered.
        self.mobile_number = mobile_number # mobile of the person that registered.
        self.image = image # Id card of the person that registered.
        self.type = type # Email of the person that registered.
        self.no_of_tickets = no_of_tickets # Number of tickets.
        self.event_name = event_name # Name of event.
        self.registration_number = registration_number # Registration number
        self.filename = ""

    def create_json(self):
        return {
            "name":self.name,
            "email":self.email,
            "mobile_number":self.mobile_number,
            #"image":json.loads(json_util.dumps(self.image))['$binary'],
            "image":self.filename,
            "type":self.type,
            "no_of_tickets":self.no_of_tickets,
            "event_name":self.event_name,
            "registration_date":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "registration_number":self.registration_number
        }

    def save_to_db(self):
        """
        Adds a new registration to database.
        Parameters:
        Returns: True/False
        """
        try:
            # Create a session with AWS.
            session = boto3.Session(
                aws_access_key_id=parser.get('AWS', 'ACCESS_KEY'),
                aws_secret_access_key=parser.get('AWS','SECRET_KEY')
                )

            #Set the session to be S3.
            connection = session.client('s3')

            #Fetch filename from the uploaded file.
            self.filename = secure_filename(self.image.filename)

            # Save the image locally.
            self.image.save(self.filename)

            # Upload image to S3.
            with open(self.filename,'rb') as f:
                connection.upload_fileobj(f, 'hackstack1.0', self.filename)

            # Create the URL for the file.
            self.filename = parser.get('AWS', 'URL')+self.filename

            # Save registration to db.
            self.registration_collection.insert_one(self.create_json())
        except errors.PyMongoError as e:
            return False
        except ClientError as e:
            return False
        except Exception as e:
            return False
        return True

    @classmethod
    def validate_registration(cls, email, event_name):
        """
        Finds if a previous registration has been made for an event with the
        same email.
        Parameters:
           1. email(str),
           2. event_names(str)
        Return: registration_details/None/False
        """
        try:
            # Return the registration details corresponding to the Parameters.
            return cls.registration_collection.find_one({"email":email,
                                                         "event_name":event_name
                                                        })
        except errors.PyMongoError as e:
            return False

    @classmethod
    def find_all_registrations(cls):
        """
        Finds every user's details from the database.
        Returns: Registration Details/None/False
        """
        try:
            # Return all the registrations from the database.
            all_registrations=list(cls.registration_collection.find({}, {"_id":0}))
            return all_registrations
        except errors.PyMongoError as e:
            return False

    @classmethod
    def find_by_registration_id(cls, registration_number, event_name_list):
        """
        Finds a user details from the database
        Parameters:
            1. registration_number(str)
            2. event_name_list(list)
        Returns: Registration Details/None/False
        """
        try:
            # Return registration for a registration_number.
            user_data = cls.registration_collection.find_one({"registration_number":registration_number,
                                                              "event_name": {"$in": event_name_list}},
                                                             {"_id":0})
            return user_data
        except errors.PyMongoError as e:
            return False

    @classmethod
    def get_registration_count_by_event(cls, event_names_list):
        """
        Finds registration count for each event from the database
        Parameters:
            1. event_names_list(list)
        Returns: list of registration count/False
        """
        try:
            count_list = []
            for event in event_names_list:
                # Find total no of tickets for each event.
                event_details = cls.registration_collection.aggregate([
                    { "$match": { "event_name": event} },
                    { "$group": {"_id":"", "event_name":{"$first":"$event_name"},
                                  "registration_count": { "$sum": "$no_of_tickets" }}}
                   ])
                # Append the ticket count and other details into a list.
                event_details = list(event_details)
                if len(event_details) == 0:
                    count_list.append({"event_name":event,
                                       "registration_count": 0})
                else:
                    count_list.append(event_details[0])
            return count_list
        except errors.PyMongoError as e:
            print(e)
            return False

    @classmethod
    def find_registration_by_event(cls, event_name):
        """
        Finds user details from the database.
        Parameters: event_name
        Returns: Registration Details/None/False
        """
        try:
            # List of all registration for an event.
            event_registrations=list(cls.registration_collection.find({"event_name": {"$in": event_name}},
                                                                      {"_id":0}))
            return event_registrations
        except errors.PyMongoError as e:
            return False

    @classmethod
    def delete_event_registrations(cls, event_name_list):
        """
        Deletes registrations for a particular event.
        Parameters:
            1. event_name_list(list)
        Returns True/False
        """
        try:
            # Delete registrations for the provided event names.
            cls.registration_collection.delete_many({"event_name":{"$in": event_name_list}})
        except errors.PyMongoError as e:
            return False
        except Exception as e:
            return False
        return True
