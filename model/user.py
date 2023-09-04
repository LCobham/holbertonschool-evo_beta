#!/usr/bin/python3
"""
    This module defines the User Class for the AirBnB clone
"""
from model.base import BaseModel


class User(BaseModel):
    """ User Class for AirBnB
        Attrs:
            - id (string): UUID4
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - email (string): email of the user
            - password (string): user hashed password using id as salt
            - first_name (string): User's first name
            - last_name (string): User's last name

        Methods:
            - constructor: Recreate a User object from a dictionary
            previously obtained with the `to_dict()` method
    """
    __required = ('email', 'password', 'first_name', 'last_name')

    def __init__(self, email, password, first_name, last_name):
        BaseModel.__init__(self)

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, mail):
        if type(mail) is not str:
            raise TypeError('email must be a string')
        self.__email = mail

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pswd):
        if type(pswd) is not str:
            raise TypeError('password must be a string')

        self.__password = pswd

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, name):
        if type(name) is not str:
            raise TypeError('first_name must be a string')
        self.__first_name = name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, surname):
        if type(surname) is not str:
            raise TypeError('last_name must be a string')
        self.__last_name = surname
