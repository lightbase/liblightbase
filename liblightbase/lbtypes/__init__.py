
# -*- coding: utf-8 -*-
from liblightbase.lbtypes.extended import FileExtension

class BaseDataType():

    def __init__(self, base, field):
        self.base = base
        self.field = field

    def __repr__(self):
        return "'%s'" % self.__class__.__name__

    def __call__(self, value):
        if self.field.required.required:
            if value == '' or value == None:
                raise Exception('Required value for "%s" not provided.' % self.field.name)
        return self.validate(value)

class RegistryId(BaseDataType):

    def __init__(self, base):
        self.base = base

    def __repr__(self):
        return "'%s'" % self.__class__.__name__

    def __call__(self, value):
        return self.base.id_reg

class File(FileExtension, BaseDataType): pass
class Document(FileExtension, BaseDataType): pass
class Sound(FileExtension, BaseDataType): pass
class Video(FileExtension, BaseDataType): pass
class Image(FileExtension, BaseDataType): pass

class Text(BaseDataType):
    def validate(self, value):
        return value

class TextArea(BaseDataType):
    def validate(self, value):
        return value

class Integer(BaseDataType):
    def validate(self, value):
        return value

class Decimal(BaseDataType):
    def validate(self, value):
        return value

class Money(BaseDataType):
    def validate(self, value):
        return value

class SelfEnumerated(BaseDataType):
    def validate(self, value):
        return value

class Date(BaseDataType):
    def validate(self, value):
        return value

class Time(BaseDataType):
    def validate(self, value):
        return value

class DateTime(BaseDataType):
    def validate(self, value):
        return value

class Url(BaseDataType):
    def validate(self, value):
        return value

class Boolean(BaseDataType):
    def validate(self, value):
        return value

class Html(BaseDataType):
    def validate(self, value):
        return value

class Email(BaseDataType):
    def validate(self, value):
        return value

class Json(BaseDataType):
    def validate(self, value):
        return value



