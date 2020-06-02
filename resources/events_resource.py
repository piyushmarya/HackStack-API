# Handles all routes for event related functionality

# Importing all required libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                get_jwt_claims)

# Importing all the required modules
from models.event_model import EventMethods
from models.event_registration_model import RegistrationMethods
from utils.status import (UNKNOWN_ERROR,
                          INSUFFICIENT_PRIVELEGES_ERROR,
                          NO_EVENT_ERROR,
                          ONGOING_EVENT_ERROR,
                          EVENT_ADD_ERROR,
                          EVENT_DELETE_ERROR,
                          EVENT_ADDED,
                          EVENT_DELETED)

# A parser to validate the request body
event_parser = reqparse.RequestParser()
event_parser.add_argument('event_name',
                    type=str,
                    help="Event name is a required field",
                    required=True)


class Events(Resource):

    @jwt_required
    def get(self):
        """
        Finds all the events from the database hosted by the admin that requests.
        Returns: List of all events
        """
         # Get the claims frpm jwt token.
        claims = get_jwt_claims()
        if claims['is_super_admin']:
            # Store list of all the events.
            event_names = EventMethods.get_events()
        else:
            # Get identity fom jwt token.
            id = get_jwt_identity()

            # Store all the events hosted by the admin in a list.
            event_names = EventMethods.get_events(id['username'])
        if event_names:
            return event_names,200
        try:
            # Check if the list is empty or None.
            if not len(event_names):
                return NO_EVENT_ERROR.to_json(), 400
        except TypeError:
            return UNKNOWN_ERROR.to_json(), 501

    @jwt_required
    def post(self):
        """
        Adds new event to the database.
        Parameters:None
        Returns: JSON message describing the status of request
        """
        # Parse the request body and stores in a dictionary.
        data = event_parser.parse_args()

        # Check if there is an ongoing event of the same name.
        event_data = EventMethods.find_by_event_name(data["event_name"])
        if event_data:
            return ONGOING_EVENT_ERROR.to_json(), 400

        # Create new event.
        if event_data is None:
            # Get identity fom jwt token and store it in the parser.
            # Fetch username from identity.
            data['username'] = get_jwt_identity()['username']
            event_obj = EventMethods(**data)
            if event_obj.save_to_db():
                return EVENT_ADDED.to_json(), 201
            return EVENT_ADD_ERROR.to_json(), 501
        return UNKNOWN_ERROR.to_json(), 501

    @jwt_required
    def delete(self):
        """
        Deletes event from the database.
        Parameters:None
        Returns: JSON message describing the status of request
        """
        # Parse the request body and stores in a dictionary.
        data = event_parser.parse_args()
        # Check if there is an ongoing event of the same name.
        event_data = EventMethods.find_by_event_name(data["event_name"])
        if event_data:
            # Get claims from jwt token.
            claims = get_jwt_claims()
            if not claims['is_super_admin']:
                # Fetch username from jwt token.
                jwt_id = get_jwt_identity()['username']
                # Check if the username in the jwt token and the username in the request
                # body is the same.
                if event_data['username'] != jwt_id:
                    return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 403
                data['username'] = jwt_id

            if claims['is_super_admin']:
                # Store the username in the parser.
                data['username'] = event_data['username']
            event_obj = EventMethods(**data)
            event_names_list = [data['event_name']]

            # Delete the event and all the registrations for that event.
            if event_obj.delete_from_db() and RegistrationMethods.delete_event_registrations(event_names_list):
                return EVENT_DELETED.to_json(), 202
            return EVENT_DELETE_ERROR.to_json(), 501

        # Check if an admin exists, but has no event hosted with provided name.
        if event_data is None:
            return NO_EVENT_ERROR.to_json(), 400
        return UNKNOWN_ERROR.to_json(), 501


class EventList(Resource):
    def get(self):
        """
        Returns all the events from database
        Parameters:None
        Return: All events,None, False
        """
        # Fetch a list of all the ongoing events.
        event_names = EventMethods.get_events()
        if event_names:
            return event_names,200
        try:
            # Check if the list is empty or None.
            if not len(event_names):
                return NO_EVENT_ERROR.to_json(), 400
        except TypeError:
            return UNKNOWN_ERROR.to_json(), 501


class EventRegistrationCount(Resource):

    @jwt_required
    def get(self):
        """
        Return a list of event and the registration count for each.
        """
        # Get claims from jwt token.
        claims = get_jwt_claims()

        # Get all events if super admin sends the request
        if claims['is_super_admin']:
            event_names = EventMethods.get_events()
        else:
            # Fetch identity from jwt token.
            id = get_jwt_identity()
            event_names = EventMethods.get_events(id['username'])
        if event_names:
            # Store all event names in a list.
            event_names_list = [i['event_name'] for i in event_names]
            # Store a count of registration in each event in a dictionary
            event_registration_count = RegistrationMethods.get_registration_count_by_event(event_names_list)
            if event_registration_count:
                return event_registration_count, 200
            return UNKNOWN_ERROR.to_json(), 501
        try:
            # Check if the list is empty or None.
            if not len(event_names):
                return NO_EVENT_ERROR.to_json(), 400
        except TypeError:
            return UNKNOWN_ERROR.to_json(), 501
