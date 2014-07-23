#!/usr/env python
# -*- coding: utf-8 -*-
from liblightbase.lbbase.lbstruct.properties import *
from liblightbase.lbutils.const import RESERVED_STRUCT_NAMES
from liblightbase.lbutils.const import PYSTR
from liblightbase import lbutils

class Field(object):

    """ The field structure holds the smallest units of information accessible. 
    """

    is_group = False
    is_field = True

    def __init__(self, name, alias, description, datatype, indices, multivalued,
            required):

        """  Field attributes
        """
        # @param name: The group name should obey the rules: 
        # No identifier can contain ASCII NUL (0x00) or a byte with a value of
        # 255. Database, table, and column names should not end with space  
        # characters. Database and table names cannot contain “/”, “\”, “.”, or 
        # characters that are not allowed in file names.
        self.name = name

        # @param alias: The field alias is a nickname for the group. It has no 
        # restriction of characters and is used for a better (human) 
        # identification of the field.
        self.alias = alias

        # @param description: Exposition, argumentation, or narration of the 
        # field existing purpose.
        self.description = description

        # @param datatype: Classification identifying one of various types of 
        # data, such as Integer or Boolean, that determines the possible values 
        # for that type.
        self.datatype = DataType(datatype)

        # @param indices: Classification of a data structure that improves the 
        # speed of data retrieval operations on a database table at the cost of 
        # additional writes and the use of more storage space to maintain the 
        # extra copy of data. Indexes are used to quickly locate data without 
        # having to search every row in a database table every time a database 
        # table is accessed. 
        self.indices = [Index(i) for i in indices]

        # @param multivalued: The multivalued property is a tipical type of 
        # NoSQL and multidimensional database. Indicates the structure capacity 
        # of holding more than one value.
        self.multivalued = Multivalued(multivalued)

        # @param required: The required property indicates that the field is one
        # in which user must enter data or not. 
        self.required = Required(required)

        self._asdict = None

    @property
    def name(self):
        """ @property name getter
        """
        return self._name

    @name.setter
    def name(self, value):
        """ @property name setter
        """
        msg = 'Invalid chars on Field name. It must be an ascii string'
        assert(isinstance(value, PYSTR)), msg
        # check ascii characters
        assert all(ord(c) < 128 for c in value), msg
        value = value.lower()
        msg = 'Field name %s is a reserved name' % value
        assert value not in RESERVED_STRUCT_NAMES, msg
        self._name = value

    @property
    def alias(self):
        """ @property alias getter
        """
        return self._alias

    @alias.setter
    def alias(self, value):
        """ @property alias setter
        """
        msg = 'Field {} alias attribute must be string or unicode!'
        assert(isinstance(value, PYSTR)), msg.format(self.name)
        self._alias = value

    @property
    def description(self):
        """ @property description getter
        """
        return self._description

    @description.setter
    def description(self, value):
        msg = 'Field {} description attribute must be string or unicode!'
        assert(isinstance(value, PYSTR)), msg.format(self.name)
        self._description= value

    @property
    def datatype(self):
        """ @property datatype getter
        """
        return self._datatype.datatype

    @datatype.setter
    def datatype(self, value):
        """ @property datatype setter
        """
        msg = 'Field {} datatype attribute must be a Datatype object.'+\
            'Instead it is {}'
        assert isinstance(value, DataType), msg.format(self.name, value)
        self._datatype = value

    @property
    def indices(self):
        """ @property indices getter
        """
        return [index.index for index in self._indices]

    @indices.setter
    def indices(self, value):
        """ @property indices setter
        """
        msg = 'Field indices attribute must be a list instead of {}'
        assert isinstance(value, list), msg.format(value)
        msg = 'Field indices elements must be instances of Indice.'
        assert all(isinstance(index, Index) for index in value)
        self._indices = value

    @property
    def multivalued(self):
        """ @property multivalued getter
        """
        return self._multivalued.multivalued

    @multivalued.setter
    def multivalued(self, value):
        """ @property multivalued setter
        """
        msg = 'Field {} multivalued attribute must instance of Multivalued.'+\
            ' Instead it is {}'
        assert isinstance(value, Multivalued), msg.format(self.name, value)
        self._multivalued = value

    @property
    def required(self):
        """ @property required getter
        """
        return self._required.required

    @required.setter
    def required(self, value):
        """ @property required setter
        """
        msg = 'Field {} required attribute must be instance of Required.'+\
            ' Instead it is %s'
        assert isinstance(value, Required), msg.format(self.name, value)
        self._required = value

    def schema(self, base, id=None):
        """ 
        A database schema is a collection of meta-data that describes the 
        relations in a database. A schema can be simply described as the
        "layout" of a database or the blueprint that outlines the way data is 
        organized into tables. This method build the field schema, returning it.
        """

        datatype = self._datatype.__schema__

        if self.multivalued is True:
            return [datatype(base, self, id)]
        elif self.multivalued is False:
            return datatype(base, self, id)
        assert False, 'Multivalued property is not True nor False, instead is \
            %s' % self.multivalued

    def document_model(self, base):
        """
        The document model is a template of the inherent structure in document.
        This method build the document model, returning it.
        """
        return self.schema(base)

    @property
    def is_rel(self):
        """ Check if field is relational
        """
        is_rel = set(['Ordenado', 'Vazio', 'Unico'])
        if len(is_rel.intersection(self.indices)) > 0:
            return True
        return False

    @property
    def asdict(self):
        """ @property asdict: Dictonary format of field model.
        """
        return {
            'field': {
                'name': self.name,
                'alias': self.alias,
                'description': self.description,
                'indices': self.indices,
                'datatype': self.datatype,
                'multivalued': self.multivalued,
                'required': self.required
            }
        }

    @property
    def json(self):
        """ @property json: JSON format of field model.
        """
        return lbutils.object2json(self.asdict)

    def metaclass(self, base, id):

        field_schema = self._datatype.__schema__
        field = self

        class FieldMetaClass(object):

            def __init__(self, value):
                self.__value__ = value

            def __setattr__(self, obj, value):
                validator = field_schema(base, field, id)
                if field.multivalued is True:
                    try:
                        assert isinstance(value, list)
                    except AssertionError:
                        msg = 'Expected type list for {}, but found {}'
                        raise ValueError(msg.format(field.name, type(value)))
                    value = [validator(element) for element in value]
                else:
                    value = validator(value)
                super(FieldMetaClass, self).__setattr__('__value__', value)

            def __getattr__(self, obj):
                return super(FieldMetaClass, self).__getattribute__('__value__')

        FieldMetaClass.__name__ = self.name
        return FieldMetaClass



