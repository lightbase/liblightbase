
from liblightbase.lbbase import fields
import json

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
    def content(self, g):
        content_list = list()
        if type(g) is list:
            for value in g:
                if isinstance(value, fields.Field) or isinstance(value, fields.Group):
                    content_list.append(value)
                else:
                    msg = 'InstanceError This should be an instance of Field or Group. instead it is %s' % value
                    raise Exception(msg)
            self._content = content_list
        else:
            msg = 'Type Error: content must be a list instead of %s' % g
            raise Exception(msg)
            self._content = None

    @property
    def object(self):

        """ Builds base object 
        """
        _metadata = dict(
            name = self.name,
            description = self.description,
        )

        _content = list()
        for attr in self.content:
            _content.append(attr.object)

        base_object= dict(
            metadata = _metadata,
            content = _content,
        )

        return base_object

    @property
    def schema(self):
        """ Builds base schema
        """

        return { attr.schema for attr in self.content }

        _schema = dict()
        for attr in self.content:
            _schema.update(attr.schema)

        return _schema

    @property
    def json(self):
        return json.dumps(self.object, ensure_ascii=True)
