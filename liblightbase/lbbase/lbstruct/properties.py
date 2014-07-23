# -*- coding: utf-8 -*-
from liblightbase.lbtypes import standard

class Index(object):

    """ 
    The index property is the classification of a data structure that improves
    the speed of data retrieval operations on a database table at the cost of 
    additional writes and the use of more storage space to maintain the extra 
    copy of data. Indexes are used to quickly locate data without having to 
    search every row in a database table every time a database table is accessed. 
    """

    # @property valid_indices: List of valid indices names
    valid_indices = [
        'Nenhum',
        'Textual',
        'Ordenado',
        'Unico',
        'Fonetico',
        'Fuzzy',
        'Vazio'
    ]

    def __init__(self, index):

        # @property index: Index type
        self.index = index

    @property
    def index(self):
        """ @property index getter 
        """
        return self._index

    @index.setter
    def index(self, value):
        """ @property index setter 
        """
        msg = '%s is not a valid Index.' % value
        assert value in self.valid_indices, msg
        self._index = value

class DataType():

    """
    The data type property is the classification identifying one of various 
    types of data, such as Integer or Boolean, that determines the possible
    values for that type. The operations that can be done on values of that
    type. The meaning of the data. The way values of that type can be stored.
    """

    # @property valid_types: List of valid data type names.
    valid_types = [
        'Boolean',
        'Date',
        'DateTime',
        'Decimal',
        'Document',
        'Email',
        'File',
        'Html',
        'Image',
        'Integer',
        'Json',
        'Money',
        'Password',
        'SelfEnumerated',
        'Sound',
        'Text',
        'TextArea',
        'Time',
        'Url',
        'Video'
    ]

    def __init__(self, datatype):

        # @property datatype: Data type
        self.datatype = datatype

        # @property __schema__:
        self.__schema__ = getattr(standard, self.datatype)

    @property
    def datatype(self):
        """ @property datatype getter
        """
        return self._datatype

    @datatype.setter
    def datatype(self, value):
        """ @property datatype setter
        """
        msg = '%s is not a valid Datatype.' % value
        assert value in self.valid_types, msg
        self._datatype = value

class Multivalued():

    """
    The multivalued property is a tipical type of NoSQL and multidimensional 
    database. Indicates the structure capacity of holding more than one value.
    """

    def __init__(self, multivalued):

        # @property multivalued: Boolean. Indicates the structure capacity of 
        # holding more than one value.
        self.multivalued = multivalued

    @property
    def multivalued(self):
        """ @property multivalued setter
        """
        return self._multivalued

    @multivalued.setter
    def multivalued(self, value):
        """ @property multivalued getter
        """
        msg = 'Multivalued attributes must be boolean.'
        assert isinstance(value, bool), msg
        self._multivalued = value

class Required():

    """ 
    In database management systems, a field can be required, optional, or 
    calculated. The required property indicates that the field is one in which
    user must enter data or not. 
    """

    def __init__(self, required):

        # @property required: Boolean. Indicates that the field is one in which
        # user must enter data or not. 
        self.required = required

    @property
    def required(self):
        """ @property required getter
        """
        return self._required

    @required.setter
    def required(self, value):
        """ @property required setter
        """
        msg = 'Required attributes must be boolean.'
        assert isinstance(value, bool), msg
        self._required = value
