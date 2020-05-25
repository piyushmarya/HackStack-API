import json
from pymongo import errors
from bson import json_util

from db import db

class EventMethods():
    collection = db.events

    def __init__(self,event_name, username):
        self.event_name = event_name
        self.username = username

    def save_to_db(self):
        """
        Adds a new event to database.
        Parameters:
        Returns: True/False
        """
        try:
            self.collection.insert_one({"event_name":self.event_name,
                                        "username":self.username
                                        })
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
        except Exception as e:
            ## TODO: Logging
            return False
        return True

    def delete_from_db(self):
        """
        Deltes event from database.
        Parameters:
        Returns: True/False
        """
        try:
            self.collection.delete_one({"event_name":self.event_name,
                                        "username":self.username
                                        })
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
        except Exception as e:
            ## TODO: Logging
            return False
        return True


    @classmethod
    def get_events(cls, username=None):
        """
        Finds every event from the database.
        Parameters:
        Returns: Event Details/None/False
        """
        try:
            if username:
                all_events=list(cls.collection.find({"username":username}))
            else:
                all_events=list(cls.collection.find({}))
            return json.loads(json_util.dumps(all_events))
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False


    @classmethod
    def find_by_event_name(cls, event_name, username=None):
        """
        Finds a administrator from the database
        Parameters:Username
        Returns: AdminDetails/None/False
        """
        try:
            return cls.collection.find_one({"event_name":event_name})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
