import json
from flask_restful import Resource, reqparse
from pymongo import errors
from bson import json_util

from utils.db import db

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

    def get(self):
        try:
            all_messages=list(self.messages_collection.find({}))
            return json.loads(json_util.dumps(all_messages)),200
        except errors.PyMongoError as e:
            ## TODO: Logging
            return {"message":"Unable to load message"},501

    def post(self):
        parser = contact_parser.parse_args()
        try:
            self.messages_collection.insert_one(parser)
            return {"message":"Thank you, Your message is sent and we will get in touch soon"}, 201
        except errors as e:
            return {"message":"Unable to send, Try again"},501
