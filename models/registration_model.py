import json
from pymongo import errors
from bson import json_util

from db import db


class RegistrationMethods:
    registration_collection=db.form_details

    @classmethod
    def find_all_registrations(cls):
        """
        Finds every user's details from the database.
        Parameters:
        Returns: Registration Details/None/False
        """
        try:
            all_registrations=list(cls.registration_collection.find({}))
            return json.loads(json_util.dumps(all_registrations))
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def find_by_registration_id(cls, registration_id):
        """
        Finds a user details from the database
        Parameters:Registration Id
        Returns: Registration Details/None/False
        """
        try:
            user_data = cls.registration_collection.find_one({"registration_id":registration_id})
            return json.loads(json_util.dumps(user_data))
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def find_count_by_registration_type(cls, registration_type):
        """
        Finds user details from the database
        Parameters:Registration Type
        Returns: Registration Type/None/False
        """
        try:
            return cls.registration_collection.count_documents({"registration_type":registration_type})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def find_registration_by_event(cls, event):
        """
        Finds user details from the database.
        Parameters:
        Returns: Registration Details/None/False
        """
        try:
            event_registrations=list(cls.registration_collection.find({"event": {"$in": event}}))
            return json.loads(json_util.dumps(event_registrations))
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
