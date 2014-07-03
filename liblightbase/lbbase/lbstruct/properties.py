
from liblightbase.lbtypes import standard

class Index():

    """ This is the index object.
    """

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
        self.index = index

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        try:
            assert value in self.valid_indices
        except AssertionError:
            raise ValueError('Supplied value for index %s is not valid' % value)
        else:
            self._index = value

class DataType():
    """ Define valid data type
    """

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
        self.datatype = datatype
        self.__schema__ = getattr(standard, self.datatype)

    @property
    def datatype(self):
        return self._datatype

    @datatype.setter
    def datatype(self, value):
        """ Check if is a valid datatype
        """
        try:
            assert value in self.valid_types
        except AssertionError:
            raise ValueError('''Wrong DataType. The value you supllied is not
                valid: %s''' % value)
        else:
            self._datatype = value

class Multivalued():
    """
    Define valid multivalued
    """
    def __init__(self, multivalued):
        self.multivalued = multivalued

    @property
    def multivalued(self):
        return self._multivalued

    @multivalued.setter
    def multivalued(self, value):
        """ Check if is a valid multivalued
        """
        try:
            assert isinstance(value, bool)
        except AssertionError:
            raise Value('''Wrong DataType. The value you supllied is not
                valid: %s''' % value)
        else:
            self._multivalued = value

class Required():
    """ Define valid required
    """
    def __init__(self, required):
        self.required = required

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value):
        """ Check if is a valid required
        """
        try:
            assert isinstance(value, bool)
        except AssertionError:
            raise ValueError('''Wrong required. The value you supllied for
                required is not valid: %s''' % value)
        else:
            self._required = value
