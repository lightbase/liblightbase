#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import datetime
from six import string_types


class School(object):
    """
    Test class to map as object
    """

    def __init__(self, name, city, country, teachers, courses, foundation_date, address=None, cep=None):
        self.name = name
        self.city = city
        self.country = country
        self.teachers = teachers
        self.courses = courses
        self.foundation_date = foundation_date
        self.address = address
        self.cep = cep


    @property
    def name(self):
        """
        name getter
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        :param value: Setter
        :return:
        """
        assert isinstance(value, string_types), "Name should be string"
        self._name = value

    @property
    def city(self):
        """
        @property city getter
        """
        return self._city

    @city.setter
    def city(self, value):
        """
        @property city setter
        """
        assert isinstance(value, string_types), "City should be string"
        self._city =  value

    @property
    def country(self):
        """
        @property country
        """
        return self._country

    @country.setter
    def country(self, value):
        """
        @property country setter
        """
        assert isinstance(value, string_types), "City should be string"
        self._country = value

    @property
    def teachers(self):
        """
        @property teachers
        """
        return self._teachers

    @teachers.setter
    def teachers(self, value):
        """
        @property teachers setter
        """
        assert isinstance(value, list), "Teachers should be a list"
        valid_keys = ['name', 'title']
        for elm in value:
            # Check if keys are valid
            assert isinstance(elm, dict), "This should be a dict"
            for key in elm.keys():
                if key not in valid_keys:
                    raise TypeError('Invalid key %s on dict',key)

        self._teachers = value



    @property
    def courses(self):
        """
        @property courses
        """
        return self._courses

    @courses.setter
    def courses(self, value):
        """
        @property courses getter
        """
        assert isinstance(value, list), "Courses should be a list"
        self._courses = value

    @property
    def foundation_date(self):
        """
        @property foundation_date
        """
        return self._foundation_date

    @foundation_date.setter
    def foundation_date(self, value):
        """
        @property foundation date setter
        """
        assert isinstance(value, datetime.datetime), "Foundation should be date"
        self._foundation_date = value