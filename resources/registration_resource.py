import urllib.parse
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from models.registration_model import RegistrationMethods
from models.event_model import EventMethods


class Registration(Resource):

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
                return{"message":"No Registrations"},400
        except TypeError:
            return{"message":"Unknown error occured"},501


class RegistrationById(Resource):

    @jwt_required
    def get(self, registration_id):
        """
        Finds registration details corresponding to id from the database.
        Parameters:Registration Id
        Returns: Registration Details
        """
        registration_details = RegistrationMethods.find_by_registration_id(registration_id)
        if registration_details:
            return registration_details,200
        if registration_details is None:
            return{"message":"No Registrations"},400
        return {"message":"Unknown error occured"},501


class RegistrationType(Resource):

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
        return {"message":"Unknown error occured"},501
