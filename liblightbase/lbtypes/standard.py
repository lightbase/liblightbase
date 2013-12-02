
# -*- coding: utf-8 -*-
from liblightbase.lbtypes import BaseDataType
from liblightbase.lbtypes.extended import FileExtension
from liblightbase import lbutils

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
    """ Represents a Image Field
    """
    pass

class Text(BaseDataType):
    """ Represents a Text Field
    """
    def validate(self, value):
        return value

class TextArea(BaseDataType):
    """ Represents a TextArea Field
    """
    def validate(self, value):
        return value

class Integer(BaseDataType):
    """ Represents a Integer Field
    """
    def validate(self, value):
        return value

class Decimal(BaseDataType):
    """ Represents a Decimal Field
    """
    def validate(self, value):
        return value

class Money(BaseDataType):
    """ Represents a Money Field
    """
    def validate(self, value):
        return value

class SelfEnumerated(BaseDataType):
    """ Represents a SelfEnumerated Field
    """
    def validate(self, value):
        return value

class Date(BaseDataType):
    """ Represents a Date Field
    """
    def validate(self, value):
        return value

class Time(BaseDataType):
    """ Represents a Time Field
    """
    def validate(self, value):
        return value

class DateTime(BaseDataType):
    """ Represents a DateTime Field
    """
    def validate(self, value):
        return value

class Url(BaseDataType):
    """ Represents a Url Field
    """
    def validate(self, value):
        return value

class Boolean(BaseDataType):
    """ Represents a Boolean Field
    """
    def validate(self, value):
        if not isinstance(value, bool):
            raise ValueError()
        return value

class Html(BaseDataType):
    """ Represents a Html Field
    """
    def validate(self, value):
        return value

class Email(BaseDataType):
    """ Represents a Email Field
    """
    def validate(self, value):
        return value

class Json(BaseDataType):
    """ Represents a Json Field
    """
    def validate(self, value):
        try:
            lbutils.parse_json(value)
        except:
            raise ValueError()
        return value
