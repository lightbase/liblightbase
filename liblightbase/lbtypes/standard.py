# -*- coding: utf-8 -*-
from liblightbase.lbtypes import BaseDataType
from liblightbase.lbtypes.extended import FileExtension
from liblightbase import lbutils
from liblightbase.lbutils.const import PYSTR
import datetime
import bcrypt

class File(FileExtension):
    """ Represents a File Field """
    pass

class Document(FileExtension):
    """ Represents a Document Field """
    pass

class Sound(FileExtension):
    """ Represents a Sound Field """
    pass

class Video(FileExtension):
    """ Represents a Video Field """
    pass

class Image(FileExtension):
    """ Represents an Image Field """
    pass

class Text(BaseDataType):
    """ Represents a Text Field """
    __dbtype__ = 'String'
    __pytype__ = str

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        self.__obj__ = value
        return value

class Password(BaseDataType):
    """ Represents a Password Field """
    __dbtype__ = 'String'
    __pytype__ = str

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            value = value.encode('utf-8')
            value = bcrypt.hashpw(value, bcrypt.gensalt())
            value = value.decode('utf-8')
            self.__obj__ = value
            # To validate later
            # value == bcrypt.hashpw(password, hashed_password)
            # will return true if the password matches
        return value

class TextArea(BaseDataType):
    """ Represents a TextArea Field """
    __dbtype__ = 'String'
    __pytype__ = str

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        self.__obj__ = value
        return value

class Integer(BaseDataType):
    """ Represents an Integer Field """
    __dbtype__ = 'Integer'
    __pytype__ = int

    @staticmethod
    def cast_str(value):
        return Integer.__pytype__(value)

    def validate(self, value):
        self.__obj__ = value
        return value

class Decimal(BaseDataType):
    """ Represents a Decimal Field """
    __dbtype__ = 'Float'
    __pytype__ = float

    @staticmethod
    def cast_str(value):
        return Decimal.__pytype__(value)

    def validate(self, value):
        self.__obj__ = value
        return value

class Money(BaseDataType):
    """ Represents a Money Field """
    __dbtype__ = 'Float'
    __pytype__ = float

    @staticmethod
    def cast_str(value):
        return Money.__pytype__(value)

    def validate(self, value):
        self.__obj__ = value
        return value

class SelfEnumerated(BaseDataType):
    """ Represents a SelfEnumerated Field """
    __dbtype__ = 'Integer'
    __pytype__ = int

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        raise NotImplementedError('type SelfEnumerated not implemented')
        self.__obj__ = value
        return value

class Date(BaseDataType):
    """ Represents a Date Field """
    __dbtype__ = 'Date'
    __pytype__ = (str, datetime.date)

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            self.__obj__ = datetime.datetime.strptime(value, '%d/%m/%Y').date()
        return value

class Time(BaseDataType):
    """ Represents a Time Field """
    __dbtype__ = 'Time'
    __pytype__ = (str, datetime.time)

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            self.__obj__ = datetime.datetime.strptime(value, '%H:%M:%S').time()
        return value

class DateTime(BaseDataType):
    """ Represents a DateTime Field """
    __dbtype__ = 'DateTime'
    __pytype__ = (str, datetime.datetime)

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            self.__obj__ = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        return value

class Url(BaseDataType):
    """ Represents an Url Field """
    __dbtype__ = 'String'
    __pytype__ = str

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        self.__obj__ = value
        return value

class Boolean(BaseDataType):
    """ Represents a Boolean Field """
    __dbtype__ = 'Boolean'
    __pytype__ = bool

    @staticmethod
    def cast_str(value):
        mapping = {True: True, False: False,
                   'y': True, 'n': False,
                   'yes': True, 'no': False,
                   't': True, 'f': False,
                   'true': True,'false': False,
                   'on': True, 'off': False,
                   '1': True, '0': False}

        if isinstance(value, PYSTR):
            value = value.lower()
        try:
            return mapping[value]
        except KeyError:
            raise ValueError('Invalid literal for boolean: "%s"' % str(value))

    def validate(self, value):
        self.__obj__ = value
        return value

class Html(BaseDataType):
    """ Represents a Html Field """
    __dbtype__ = 'String'
    __pytype__ = str

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        self.__obj__ = value
        return value

class Email(BaseDataType):
    """ Represents an Email Field """
    __dbtype__ = 'String'
    __pytype__ = str

    @staticmethod
    def cast_str(value):
        return value

    def validate(self, value):
        self.__obj__ = value
        return value

class Json(BaseDataType):
    """ Represents a Json Field """
    __dbtype__ = 'String'
    __pytype__ = (int, bool, float, list, dict, str, type(None))

    @staticmethod
    def cast_str(value):
        return lbutils.json2object(value)

    def validate(self, value):
        lbutils.object2json(value)
        self.__obj__ = value
        return value
