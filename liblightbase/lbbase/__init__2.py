
from liblightbase.lbbase import fields
import json
from voluptuous import Schema

class Base():
    """
    Defining a LB Base object
    """
    def __init__(self, name, description, content, **entries):
        """
        Base attributes
        """
        self.name = name
        self.description = description
        self.content = content
        if entries:
            self.__dict__.update(entries)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, c):
        content_list = list()
        if type(c) is list:
            for value in c:
                if isinstance(value, fields.Field) or isinstance(value, fields.Group):
                    content_list.append(value)
                else:
                    msg = 'InstanceError This should be an instance of Field or Group. instead it is %s' % value
                    raise Exception(msg)
            self._content = content_list
        else:
            msg = 'Type Error: content must be a list instead of %s' % c
            raise Exception(msg)
            self._content = None

    @property
    def object(self):
        """ Builds base object 
        """
        return dict(
            content = [attr.object for attr in self.content],
            metadata = dict(
                name = self.name,
                description = self.description,
            )
        )

    @property
    def schema(self):
        """ Builds base Schema
        """
        return Schema({attr.name: attr.schema for attr in self.content})

    @property
    def json(self):
        """ Builds base JSON
        """
        return json.dumps(self.object, ensure_ascii=True)
