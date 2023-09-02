#!/usr/bin/python3
"""
    This module defines the UserService class,
    containing the business logic for the user class.
"""
from service.service import ServiceBase
from model.user import User


class UserService(ServiceBase):
    """
        UserService Class. Handles business logic for users
    """
    __service_class = User

    def validate_mail_is_unique(self, email):
        users = self.all().values()

        search_email = list(filter(lambda x: x.email == email, users))
        
        if search_email:
            raise ValueError('email is not unique')

    def create(self, **inputs):
        self.validate_mail_is_unique(inputs.get('email'))
        return ServiceBase.create(self, **inputs)

    def update(self, id, **inputs):
        if 'email' in inputs.keys():
            self.validate_mail_is_unique(inputs.get('email'))

        return ServiceBase.update(self, id, **inputs)