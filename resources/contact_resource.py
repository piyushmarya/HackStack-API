import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from pymongo import errors

from utils.db import db
from utils.status import (MESSAGE_LOAD_ERROR,
                         MESSAGE_SENT,
                         INSUFFICIENT_PRIVELEGES_ERROR,
                         MESSAGE_SEND_ERROR,
                         MESSAGE_DELETED,
                         MESSAGE_DELETE_ERROR)

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
        try:
            claims = get_jwt_claims()
            if claims['is_admin']:
                all_messages=list(self.messages_collection.find({},{"_id":0}))
                return all_messages, 200
            else:
                return INSUFFICIENT_PRIVELEGES_ERROR.to_json(),400
        except errors.PyMongoError as e:
            ## TODO: Logging
            return MESSAGE_LOAD_ERROR.to_json(),501

    def post(self):
        parser = contact_parser.parse_args()
        try:
            self.messages_collection.insert_one(parser)
            return MESSAGE_SENT.to_json(), 201
        except errors as e:
            return MESSAGE_SEND_ERROR.to_json(),501

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if claims['is_admin']:
            parser = contact_parser.parse_args()
            try:
                self.messages_collection.delete_one(parser)
                return MESSAGE_DELETED.to_json(), 201
            except errors.PyMongoError as e:
                return MESSAGE_DELETE_ERROR.to_json(),501
        return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 400
