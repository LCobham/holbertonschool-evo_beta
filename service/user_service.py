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

    @classmethod
    def validate_mail_is_unique(cls, email):
        users = cls.all().values()

        search_email = list(filter(lambda x: x.email == email, users))
        
        if search_email:
            raise ValueError('email is not unique')

    @classmethod
    def create(cls, **inputs):
        cls.validate_mail_is_unique(inputs.get('email'))
        return cls.create_base(**inputs)

    @classmethod
    def update(cls, id, **inputs):
        if 'email' in inputs.keys():
            cls.validate_mail_is_unique(inputs.get('email'))

        return cls.update_base(id, **inputs)
