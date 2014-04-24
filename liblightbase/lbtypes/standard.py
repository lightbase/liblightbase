
# -*- coding: utf-8 -*-
from liblightbase.lbtypes import BaseDataType
from liblightbase.lbtypes.extended import FileExtension
from liblightbase import lbutils
import datetime

class File(FileExtension):
    """ Represents a File Field
    """
    pass

class Document(FileExtension):
    """ Represents a Document Field
    """
    pass

class Sound(FileExtension):
    """ Represents a Sound Field
    """
    pass

class Video(FileExtension):
    """ Represents a Video Field
    """
    pass

class Image(FileExtension):
    """ Represents an Image Field
    """
    pass

class Text(BaseDataType):
    """ Represents a Text Field
    """
    __pytype__ = str

    def validate(self, value):
        self.__obj__ = value
        return value

class TextArea(BaseDataType):
    """ Represents a TextArea Field
    """
    __pytype__ = str

    def validate(self, value):
        self.__obj__ = value
        return value

class Integer(BaseDataType):
    """ Represents an Integer Field
    """
    __pytype__ = int

    def validate(self, value):
        self.__obj__ = value
        return value

class Decimal(BaseDataType):
    """ Represents a Decimal Field
    """
    __pytype__ = float

    def validate(self, value):
        self.__obj__ = value
        return value

class Money(BaseDataType):
    """ Represents a Money Field
    """
    __pytype__ = float

    def validate(self, value):
        self.__obj__ = value
        return value

class SelfEnumerated(BaseDataType):
    """ Represents a SelfEnumerated Field
    """
    __pytype__ = int

    def validate(self, value):
        raise NotImplementedError('type SelfEnumerated not implemented')
        self.__obj__ = value
        return value

class Date(BaseDataType):
    """ Represents a Date Field
    """
    __pytype__ = (str, datetime.date)

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            self.__obj__ = datetime.datetime.strptime(value, '%d/%m/%Y').date()
        return value

class Time(BaseDataType):
    """ Represents a Time Field
    """
    __pytype__ = (str, datetime.time)

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            self.__obj__ = datetime.datetime.strptime(value, '%H:%M:%S').time()
        return value

class DateTime(BaseDataType):
    """ Represents a DateTime Field
    """
    __pytype__ = (str, datetime.datetime)

    def validate(self, value):
        if value == '':
            self.__obj__ = value
        else:
            self.__obj__ = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        return value

class Url(BaseDataType):
    """ Represents an Url Field
    """
    __pytype__ = str

    def validate(self, value):
        self.__obj__ = value
        return value

class Boolean(BaseDataType):
    """ Represents a Boolean Field
    """
    __pytype__ = bool

    def validate(self, value):
        self.__obj__ = value
        return value

class Html(BaseDataType):
    """ Represents a Html Field
    """
    __pytype__ = str

    def validate(self, value):
        self.__obj__ = value
        return value

class Email(BaseDataType):
    """ Represents an Email Field
    """
    __pytype__ = str

    def validate(self, value):
        self.__obj__ = value
        return value

class Json(BaseDataType):
    """ Represents a Json Field
    """
    __pytype__ = (int, bool, float, list, dict)

    def validate(self, value):
        lbutils.object2json(value)
        self.__obj__ = value
        return value
