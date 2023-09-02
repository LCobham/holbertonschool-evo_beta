#!/usr/bin/python3
"""
    This module defines the CountryService class
    with the business logic related to the Country
    class
"""

from model.country import Country
from service.service import ServiceBase


class CountryService(ServiceBase):
    """
        Country service class for Country business logic
    """
    __service_class = Country