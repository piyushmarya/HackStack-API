# Routes for all messages related functionality.

# Importing all required libraries.
import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from pymongo import errors

# Importing all required modules.
from utils.db import db
from utils.status import (MESSAGE_LOAD_ERROR,
                         MESSAGE_SENT,
                         INSUFFICIENT_PRIVELEGES_ERROR,
                         MESSAGE_SEND_ERROR,
                         MESSAGE_DELETED,
                         MESSAGE_DELETE_ERROR)

# A parser to validate the request body
contact_parser = reqparse.RequestParser()
contact_parser.add_argument('name',
                    type=str,
                    help="Username is a required field",
                    required=True)
contact_parser.add_argument('email',
                    type=str,
                    help="Username is a required field",
                    required=True)
contact_parser.add_argument('message',
                    type=str,
                    help="message is a required field",
                    required=True)


class ContactAdmin(Resource):
    messages_collection = db.messages

    @jwt_required
    def get(self):
        """
        Fetch messages from db.
        Returns : List of messages
        """
        try:
            # Get claims from the jwt token.
            claims = get_jwt_claims()

            # Check if jwt token provided is by the super admin.
            if claims['is_super_admin']:

                # Create a list of all the messages.
                all_messages=list(self.messages_collection.find({},{"_id":0}))
                return all_messages, 200
            else:
                return INSUFFICIENT_PRIVELEGES_ERROR.to_json(),400
        except errors.PyMongoError as e:
            ## TODO: Logging
            return MESSAGE_LOAD_ERROR.to_json(),501

    def post(self):
        """
        Adds a message to db.
        Returns : JSON message containing the status of request.
        """
        # Parse, validate request body and store it in a dictionary..
        parser = contact_parser.parse_args()
        try:
            #Insert the message into the database.
            self.messages_collection.insert_one(parser)
            return MESSAGE_SENT.to_json(), 201
        except errors.PyMongoError as e:
            return MESSAGE_SEND_ERROR.to_json(),501

    @jwt_required
    def delete(self):
        """
        Delete a message from db.
        Returns : JSON message containing the status of request.
        """
        # Get claims from the jwt token.
        claims = get_jwt_claims()

        # Check if the request is made by the super admin.
        if claims['is_super_admin']:
            # Parse, validate request body and store it in a dictionary.
            parser = contact_parser.parse_args()
            try:
                # Delete the message.
                self.messages_collection.delete_one(parser)
                return MESSAGE_DELETED.to_json(), 201
            except errors.PyMongoError as e:
                return MESSAGE_DELETE_ERROR.to_json(),501
        return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 400
