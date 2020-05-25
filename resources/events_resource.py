from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                get_jwt_claims)

from models.event_model import EventMethods

event_parser = reqparse.RequestParser()
event_parser.add_argument('event_name',
                    type=str,
                    help="Event name is a required field",
                    required=True)


class Events(Resource):

    @jwt_required
    def get(self):
        """
        Finds all the events from the database based on the user that requests.
        Parameters:None
        Returns: List of all events
        """
        claims = get_jwt_claims()
        if claims['is_admin']:
            event_names = EventMethods.get_events()
        else:
            id = get_jwt_identity()
            event_names = EventMethods.get_events(id['username'])
        if event_names:
            return event_names,200
        try:
            if not len(event_names):
                return{"message":"No Events"},400
        except TypeError:
            return{"message":"Unknown error occured, Try again in some time"},501

    @jwt_required
    def post(self):
        """
        Adds new event to the database.
        Parameters:None
        Returns: JSON message describing the status of request
        """
        data = event_parser.parse_args()
        event_data = EventMethods.find_by_event_name(data["event_name"])
        if event_data:
            return {"message":"It is an ongoing event,change event name"},400
        if event_data is None:
            data['username'] = get_jwt_identity()['username']
            event_obj = EventMethods(**data)
            if event_obj.save_to_db():
                return {"message":"Event Added"},201
            return {
                "message":"Unknown error occured while registring.Try Again"
                },501
        return{"message" : "Unknown error occured"},501

    @jwt_required
    def delete(self):
        """
        Deletes event from the database.
        Parameters:None
        Returns: JSON message describing the status of request
        """
        data = event_parser.parse_args()
        event_data = EventMethods.find_by_event_name(data["event_name"])
        if event_data:
            claims = get_jwt_claims()
            if not claims['is_admin']:
                jwt_id = get_jwt_identity()['username']
                if event_data['username'] != jwt_id:
                    return {"message":"Unauthorized"},401
                data['username'] = jwt_id
            if claims['is_admin']:
                data['username'] = event_data['username']
            event_obj = EventMethods(**data)
            if event_obj.delete_from_db():
                return {"message":"Event deleted"},202
            return {"message":"Unknown error occured while deleting, Try again in some time"},501
        if event_data is None:
            return {"message":"No event found"},400
        return {"message":"Unknown error occured"},501


class EventList(Resource):
    def get(self):
        """
        Returns all the events from database
        Parameters:None
        Return: All events,None, False
        """
        event_names = EventMethods.get_events()
        if event_names:
            return event_names,200
        try:
            if not len(event_names):
                return{"message":"No Events"},400
        except TypeError:
            return{"message":"Unknown error occured"},501
