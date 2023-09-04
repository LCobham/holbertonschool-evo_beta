#!/usr/bin/python3
"""
    This module defines the UserService class,
    containing the business logic for the user class.
"""
from service.service import ServiceBase
from model.user import User
from model import storage
import os
from hashlib import pbkdf2_hmac
# Implementing simple proof od concept for password hashing

# OWASP Recommended iteations for pbkf2 sha256 is 600.000
# (Note that unittests would run very slow if implementing
# that many iterations)
if os.environ.get('TESTING'):
    HASH_ITERATIONS = 1
else:
    HASH_ITERATIONS = 600_000


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
        if 'email' in inputs.keys():
            cls.validate_mail_is_unique(inputs.get('email'))

        service_cls = cls.service_class()
        required_inputs = service_cls.required()

        # Get only relevant information
        subset = {key: inputs[key] for key in required_inputs}

        new_instance = service_cls(**subset)
        new_instance.password = cls.pswd_hash(
            new_instance.id, new_instance.password
        )

        storage.add(new_instance)
        storage.save()

        return new_instance

    @classmethod
    def update(cls, id, **inputs):
        if 'email' in inputs.keys():
            cls.validate_mail_is_unique(inputs.get('email'))
        
        if 'password' in inputs.keys():
            inputs['password'] = cls.pswd_hash(id, inputs['password'])

        return cls.update_base(id, **inputs)

    @staticmethod
    def pswd_hash(user_id, pswd):
        if type(user_id) is not str or type(pswd) is not str:
            raise TypeError('user_id and pswd must be strings')

        # Probably not a good practice to use UUID4 as salt but
        # good enough for proof of concept

        hash = pbkdf2_hmac(
            'sha256', pswd.encode('utf-8'),
            user_id.encode('utf-8'), HASH_ITERATIONS
        )

        return hash.hex()
