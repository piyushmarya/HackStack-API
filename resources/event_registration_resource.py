# Handles all required routes for event registration related functionality.

# Importing all required libraries.
from flask_restful import Resource,reqparse
from flask import request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from uuid import uuid4
from werkzeug.datastructures import FileStorage

# Importing all the required modules.
from models.event_registration_model import RegistrationMethods
from models.event_model import EventMethods

from utils.status import (NO_REGISTRATIONS_ERROR,
                          UNKNOWN_ERROR,
                          INSUFFICIENT_PRIVELEGES_ERROR,
                          REGISTRATION_EXISTS_ERROR)


class EventRegistration(Resource):
    """Add or fetch registrations for an event."""

    # A parser to validate the request body
    registration_parser = reqparse.RequestParser()
    registration_parser.add_argument('name',
                        help="name is a required field",
                        required=True,
                        location='form')
    registration_parser.add_argument('email',
                        type=str,
                        help="Email is a required field",
                        required=True,
                        location='form')
    registration_parser.add_argument('type',
                        type=str,
                        help="registration type is a required field",
                        required=True,
                        location='form')
    registration_parser.add_argument('no_of_tickets',
                        type=int,
                        help="Number of tickets is a required field",
                        required=True,
                        location='form')
    registration_parser.add_argument('event_name',
                        type=str,
                        help="Event name is a required field",
                        required=True,
                        location='form')
    registration_parser.add_argument('mobile_number',
                        type=str,
                        help="Mobile number is a required field",
                        required=True,
                        location='form')
    registration_parser.add_argument('image',
                        type=FileStorage,
                        help="Image is a required field",
                        required=True,
                        location='files')

    @jwt_required
    def get(self):
        """
        Finds all user registrations from the database
        Parameters:None
        Returns: Registrations
        """
        # Get the claims frpm jwt token.
        claims = get_jwt_claims()
        if claims['is_super_admin']:
            # Store all the registrations in a list.
            all_registrations = RegistrationMethods.find_all_registrations()
        else:
            #Get identity fom jwt token.
            username = get_jwt_identity()['username']
            event_names = EventMethods.get_events(username)

            # Store all the events in a list.
            event=[ i["event_name"] for i in event_names]
            # Store all the registrations for the events in a list.
            all_registrations = RegistrationMethods.find_registration_by_event(event)
        if all_registrations:
            return all_registrations,200
        try:
            # Check if the list is empty or None.
            if not(len(all_registrations)):
                return NO_REGISTRATIONS_ERROR.to_json(), 400
        except TypeError:
            return UNKNOWN_ERROR.to_json(), 501

    def post(self):
        """
        Add new registration to the database.
        Return:Request Status
        """
        # Parse the request body and stores in a dictionary.
        data = self.registration_parser.parse_args()

        # Check if a registration with same email for an event has been created before.
        registration_details = RegistrationMethods.validate_registration(data['email'],
                                                                         data['event_name'])
        if registration_details is not None:
            return REGISTRATION_EXISTS_ERROR.to_json(), 400
        elif registration_details is None:
            # Creating registration number.
            data['registration_number'] = uuid4().hex
            registration_obj = RegistrationMethods(**data)
            if registration_obj.save_to_db():
                return {"registration_number":data['registration_number']},201
            else:
                return UNKNOWN_ERROR.to_json(), 501
        else:
            return UNKNOWN_ERROR.to_json(), 501


class EventRegistrationByNumber(Resource):

    @jwt_required
    def get(self, registration_number):
        """
        Finds registration details corresponding to id from the database.
        Parameters:
            1. Registration Number(String)
        Returns: Registration Details
        """
        # Get claims from the jwt token.
        claims = get_jwt_claims()
        if claims['is_super_admin']:
            # Store all events in a list.
            event_names = EventMethods.get_events()
        else:
            # Fetch username from jwt token.
            username = get_jwt_identity()['username']
            # Get a dictionary event names hosted by the admin.
            event_names = EventMethods.get_events(username)

        if event_names:
            # Created a list of all event names.
            event_name_list=[ i["event_name"] for i in event_names]
            #Find the registration details using the registration_number
            # and event name list.
            registration_details = RegistrationMethods.find_by_registration_id(registration_number, event_name_list)
            if registration_details:
                return registration_details,200
            if registration_details is None:
                return NO_REGISTRATIONS_ERROR.to_json(), 400
            return UNKNOWN_ERROR.to_json(), 501
        return NO_REGISTRATIONS_ERROR.to_json(), 400
