
# Importing all required libraries
import json
from passlib.hash import sha256_crypt
from pymongo import errors

# Importing all the required modules.
from utils.db import db
from utils.config_parser import parser

class AdminMethods:
    """Consists all methods for admin related functionality."""

    # Getting the name of the collection in which the admin details are stored.
    admin_collection = db.admins

    def __init__(self,username, password, uuid=None):
        self.username = username #Username of admmin
        self.password = sha256_crypt.encrypt(password) # Password for the admin.
        self.uuid = uuid # UUID for the admin.

    def create_json(self):
        """
        Creates json of instance variables.
        Parameters:
        Returns: JSON of instance variables.
        """
        return {
            "username":self.username,
            "password":self.password,
            "uuid":self.uuid
            }

    def change_pwd(self):
        """
        Updates password in the database.
        Parameters:
        Returns: True/False
        """
        try:
            # Updating the password for the provided username.
            self.admin_collection.update_one({"username":self.username},
                                       {"$set":{"password":self.password}})
        except errors.PyMongoError as e:
            return False
        except Exception as e:
            return False
        return True

    def save_to_db(self):
        """
        Adds a new administrator to database.
        Parameters:
        Returns: True/False
        """
        try:
            # Inserting the dictionary returned from create_json() method.
            self.admin_collection.insert_one(self.create_json())
        except errors.PyMongoError as e:
            return False
        except Exception as e:
            return False
        return True

    @classmethod
    def delete_admin(cls, username):
        """
        Deletes administrator from database.
        Parameters:
            1. username(string): username of the admin.
        Returns: True/False
        """
        try:
            # Delete the admin with username that matches.
            cls.admin_collection.delete_one({"username":username})
        except errors.PyMongoError as e:
            return False
        except Exception as e:
            return False
        return True

    @classmethod
    def fetch_by_username(cls, username):
        """
        Finds a administrator from the database
        Parameters:
            1. username(string): username of the admin.
        Returns: AdminDetails/None/False
        """
        try:
            # Return the information of admin corresponding to the username.
            return cls.admin_collection.find_one({"username":username})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def fetch_by_uuid(cls, uuid):
        """
        Finds a administrator from the database
        Parameters:
            1. uuid(string): uuid of the admin.
        Returns: AdminDetails/None/False
        """
        try:
            # Return the information of admin corresponding to the uuid.
            return cls.admin_collection.find_one({"uuid":uuid})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def get_all_admins(cls):
        """
        Finds all administrators from the database
        Parameters:
        Returns: AdminDetails/False
        """
        try:
            # Create a list of all admins in db excluding the super admin.
            all_users = list(cls.admin_collection.find({"username":{"$nin":[parser.get('API', 'ADMIN_NAME')]}},
                                                       { "_id":0, "password":0}))
            return all_users
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
