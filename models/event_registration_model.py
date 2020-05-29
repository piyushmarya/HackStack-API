import json
from pymongo import errors
import boto3
from botocore.exceptions import ClientError
from configparser import ConfigParser
from datetime import datetime
from werkzeug.utils import secure_filename

from utils.db import db


class RegistrationMethods:
    registration_collection=db.form_details

    def __init__(self, name, email, mobile_number, image, type, no_of_tickets,
                 event_name, registration_number):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.image = image
        self.type = type
        self.no_of_tickets = no_of_tickets
        self.event_name = event_name
        self.registration_number = registration_number
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
            parser = ConfigParser()
            parser.read('configurations/config.ini')
            session = boto3.Session(
                aws_access_key_id=parser.get('AWS', 'ACCESS_KEY'),
                aws_secret_access_key=parser.get('AWS','SECRET_KEY')
                )
            connection = session.client('s3')
            self.filename = secure_filename(self.image.filename)
            self.image.save(self.filename)
            with open(self.filename,'rb') as f:
                connection.upload_fileobj(f, 'hackstack1.0', self.filename)
            self.filename = parser.get('AWS', 'URL')+self.filename
            self.registration_collection.insert_one(self.create_json())
        except errors.PyMongoError as e:
             ## TODO: Logging
            print(e)
            return False
        except ClientError as e:
            print(e)
            return False
        except Exception as e:
             ## TODO: Logging
            print(e)
            return False
        return True

    @classmethod
    def validate_registration(cls, email, event_name):
        """
        Finds if a previous registration has been made for an event with the
        same email.
        Parameters:email,event_names
        Return: registration_details/None/False
        """
        try:
            return cls.registration_collection.find_one({"email":email,
                                                         "event_name":event_name
                                                        })
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def find_all_registrations(cls):
        """
        Finds every user's details from the database.
        Parameters:
        Returns: Registration Details/None/False
        """
        try:
            all_registrations=list(cls.registration_collection.find({}, {"_id":0}))
            return all_registrations
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def find_by_registration_id(cls, registration_number, event_name):
        """
        Finds a user details from the database
        Parameters:Registration Id
        Returns: Registration Details/None/False
        """
        try:
            user_data = cls.registration_collection.find_one({"registration_number":registration_number,
                                                              "event_name": {"$in": event_name}},
                                                             {"_id":0})
            return user_data
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def get_registration_count_by_event(cls, event_names_list):
        """
        Finds registration count for each event from the database
        Parameters:event_names_list
        Returns: list of registration count/False
        """
        try:
            count_list = []
            for event in event_names_list:
                event = cls.registration_collection.aggregate([
                     { "$match": { "event_name": event} },
                     { "$group": {"_id":"&id","event_name":{"$first":"$event_name"},
                                  "registration_count": { "$sum": "$no_of_tickets" }}}
                   ])
                count_list.append(list(event)[0])
            return count_list
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def find_registration_by_event(cls, event_name):
        """
        Finds user details from the database.
        Parameters: event_name
        Returns: Registration Details/None/False
        """
        try:
            event_registrations=list(cls.registration_collection.find({"event_name": {"$in": event_name}},{"_id":0}))
            return json.loads(json_util.dumps(event_registrations))
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def delete_event_registrations(cls, event_name):
        """
        Deletes registrations for a particular event.
        Parameters: event_name
        Returns True/False
        """
        try:
            cls.registration_collection.delete_many({"event_name":event_name})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
        except Exception as e:
            ## TODO: Logging
            return False
        return True
