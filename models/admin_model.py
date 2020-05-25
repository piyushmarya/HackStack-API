from passlib.hash import sha256_crypt
from pymongo import errors

from db import db


class AdminMethods:
    collection = db.admins

    def __init__(self,username, password, uuid=None):
        self.username = username
        self.password = sha256_crypt.encrypt(password)
        self.uuid = uuid

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
            self.collection.update_one({"username":self.username},
                                       {"$set":{"password":self.password}})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
        except Exception as e:
            ## TODO: Logging
            return False
        return True

    def save_to_db(self):
        """
        Adds a new administrator to database.
        Parameters:
        Returns: True/False
        """
        try:
            self.collection.insert_one(self.create_json())
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
        except Exception as e:
            ## TODO: Logging
            return False
        return True

    def delete_admin(self):
        """
        Deletes administrator from database.
        Parameters:
        Returns: True/False
        """
        try:
            self.collection.delete_one(self.create_json())
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
        except Exception as e:
            ## TODO: Logging
            return False
        return True

    @classmethod
    def fetch_by_username(cls, username):
        """
        Finds a administrator from the database
        Parameters:Username
        Returns: AdminDetails/None/False
        """
        try:
            return cls.collection.find_one({"username":username})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False

    @classmethod
    def fetch_by_uuid(cls, uuid):
        """
        Finds a administrator from the database
        Parameters:Unique user id
        Returns: AdminDetails/None/False
        """
        try:
            return cls.collection.find_one({"uuid":uuid})
        except errors.PyMongoError as e:
            ## TODO: Logging
            return False
