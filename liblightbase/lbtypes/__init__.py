
# -*- coding: utf-8 -*-

class BaseDataType():

    """ Base Methods for any Field
    """
    def __init__(self, base, field, id):
        self.base = base
        self.field = field
        self.id = id

    def __repr__(self):
        return '%s' % self.__class__.__name__

    def __call__(self, value):
        if self.field.required.required:
            if value == '' or value == None:
                raise Exception('Required value for "%s" not provided.' % self.field.name)
        return self.validate(value)

