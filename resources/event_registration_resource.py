from flask_restful import Resource,reqparse
from flask import request,jsonify
from uuid import uuid4
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from models.event_registration_model import RegistrationMethods
from models.event_model import EventMethods
from utils.status import (NO_REGISTRATIONS_ERROR,
                          UNKNOWN_ERROR,
                          INSUFFICIENT_PRIVELEGES_ERROR,
                          REGISTRATION_EXISTS_ERROR)


class EventRegistration(Resource):
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
                        type=str,
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
        claims = get_jwt_claims()
        if claims['is_admin']:
            event_names = EventMethods.get_events()
            all_registrations = RegistrationMethods.find_all_registrations()
        else:
            id = get_jwt_identity()['username']
            event_names = EventMethods.get_events(id)
            event=[ i["event_name"] for i in event_names]
            all_registrations = RegistrationMethods.find_registration_by_event(event)

        if all_registrations:
            return all_registrations,200
        try:
            if not(len(all_registrations)):
                return NO_REGISTRATIONS_ERROR.to_json(), 400
        except TypeError:
            return UNKNOWN_ERROR.to_json(), 501

    def post(self):
        """
        Add new registration to the database.
        Return:Request Status
        """
        data = self.registration_parser.parse_args()
        registration_details = RegistrationMethods.validate_registration(data['email'],
                                                                         data['event_name'])
        if registration_details is not None:
            return REGISTRATION_EXISTS_ERROR.to_json(), 400
        elif registration_details is None:
            data['registration_number'] = uuid4().hex
            registration_obj = RegistrationMethods(**data)
            if registration_obj.save_to_db():
                return {"registration_number":data['registration_number']},201
            else:
                return UNKNOWN_ERROR.to_json(), 501
        else:
            return UNKNOWN_ERROR.to_json(), 501


class EventRegistrationById(Resource):

    @jwt_required
    def get(self, registration_id):
        """
        Finds registration details corresponding to id from the database.
        Parameters:Registration Id
        Returns: Registration Details
        """
        claims = get_jwt_claims()
        if claims['is_admin']:
            event_names = EventMethods.get_events()
        else:
            username = get_jwt_identity()['username']
            event_names = EventMethods.get_events(username)
        if event_names:
            event=[ i["event_name"] for i in event_names]
            registration_details = RegistrationMethods.find_by_registration_id(registration_id, event)
            if registration_details:
                return registration_details,200
            if registration_details is None:
                return NO_REGISTRATIONS_ERROR.to_json(), 400
            return UNKNOWN_ERROR.to_json(), 501
        return NO_REGISTRATIONS_ERROR.to_json(), 400


class EventRegistrationType(Resource):

    @jwt_required
    def get(self, event_name):
        """
        Finds the count of every registration type from the database.
        Parameters:None
        Returns: Registration Type Count/
        """
        claims = get_jwt_claims()
        if claims['is_admin']:
            event_names = EventMethods.get_events()
            count_list = [RegistrationMethods.find_count_by_registration_type(i) for i in ["self", "corporate", "others", "group"]]
            if all(count_list):
                return {"self":count_list[0],
                    "corporate":count_list[1],
                    "others": count_list[2],
                    "group" :count_list[3]
                },200
        return INSUFFICIENT_PRIVELEGES_ERROR.to_json(), 403
