
import voluptuous
from liblightbase.lbtypes import standard

class Group():
    """
    This is the field description
    """
    def __init__(self, name, alias, description, content, multivalued):
        """
        Group attributes
        """
        self.name = name
        self.alias = alias
        self.description = description
        self.content = content
        self.multivalued = multivalued

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, c):
        content_list = list()
        if type(c) is list:
            for value in c:
                if isinstance(value, Field) or isinstance(value, Group):
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
    def multivalued(self):
        return self._multivalued

    @multivalued.setter
    def multivalued(self, m):
        if isinstance(m, Multivalued):
            self._multivalued = m
        else:
            # Invalid multivalued. Raise exception
            msg = 'InstanceError This should be an instance of Multivalued. instead it is %s' % m
            raise Exception(msg)
            self._multivalued = None

    @property
    def object(self):
        """ Builds group object 
        """
        return dict(
            group = dict(
                content = [attr.object for attr in self.content],
                metadata = dict(
                    name = self.name,
                    alias = self.alias,
                    description = self.description,
                    multivalued =  self.multivalued.multivalued
                )
            )
        )

    @property
    def schema(self):
        """ Builds base schema
        """
        _schema = dict()
        for attr in self.content:
            required = getattr(attr, 'required', False)
            if required and required.required is True:
                _schema[voluptuous.Required(attr.name)] = attr.schema
            else:
                _schema[attr.name] = attr.schema
        if self.multivalued.multivalued is True:
            return [_schema]
        elif self.multivalued.multivalued is False:
            return _schema

class Field():
    """
    This is the field description
    """
    def __init__(self, name, alias, description, datatype, indices, multivalued, required):
        """
        Field attributes
        """
        self.name = name
        self.alias = alias
        self.description = description
        self.datatype = datatype
        self.indices = indices
        self.multivalued = multivalued
        self.required = required

    @property
    def datatype(self):
          return self._datatype

    @datatype.setter
    def datatype(self, t):
        """
        check this attribute properties
        """
        if isinstance(t, DataType):
            self._datatype = t
        else:
            msg = 'TypeError This must be a instance of datatype. Instead it is %s' % t
            raise Exception(msg)
            self._datatype = None

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, i):
        """
        Validate the value for this field
        """
        indices_list = list()
        if type(i) is list:
            for value in i:
                if isinstance(value, Index):
                    indices_list.append(value)
                else:
                    msg = 'InstanceError This should be an instance of Indice. instead it is %s' % value
                    raise Exception(msg)
            self._indices = indices_list
        else:
            # Invalid index. Raise exception
            msg = 'Type Error: indexes must be a list instead of %s' % i
            raise Exception(msg)
            self._indices = None

    @property
    def multivalued(self):
        return self._multivalued

    @multivalued.setter
    def multivalued(self, m):
        if isinstance(m, Multivalued):
            self._multivalued = m
        else:
            # Invalid multivalued. Raise exception
            msg = 'InstanceError This should be an instance of Multivalued. instead it is %s' % m
            raise Exception(msg)
            self._multivalued = None

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, r):
        if isinstance(r, Required):
            self._required = r
        else:
            # Invalid required. Raise exception
            msg = 'InstanceError This should be an instance of Required. instead it is %s' % r
            raise Exception(msg)
            self._required = None

    @property
    def object(self):

        """ Builds field object 
        """
        _field = dict(
            name = self.name,
            alias = self.alias,
            description = self.description,
            indices = [i.index for i in self.indices],
            datatype = self.datatype.datatype,
            multivalued = self.multivalued.multivalued,
            required = self.required.required
        )
        return dict(field = _field)

    @property
    def schema(self):

        """ Builds field schema
        """
        datatype = getattr(standard, self.datatype.datatype.replace('/', ''))

        if self.multivalued.multivalued is True:
            return [datatype()]
        elif self.multivalued.multivalued is False:
            return datatype()
        else:
            raise Exception('multivalued must be boolean')

class Index():
    """
    This is the index object.
    """
    def __init__(self, index):
        self.index = index

    def valid_indices(self):
        """
        Returns a list of valid values for indices
        """
        # TODO: Get this list of values from somewhere else
        valid_indices = ['Nenhum',
                         'Textual',
                         'Ordenado',
                         'Unico',
                         'Fonetico',
                         'Fuzzy',
                         'Vazio',
                         ]

        return valid_indices

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, i):
        if not i in self.valid_indices():
            # invalid value for indices. Raise exception
            msg = 'IndexError violation. Supplied value for index %s is not valid' % i
            raise Exception(msg)
            self._index = None

        self._index = i

class DataType():
    """
    Define valid data type
    """
    def __init__(self, datatype):
        self.datatype = datatype

    def valid_types(self):
        """
        Get valid instances of pototypes
        """
        # TODO: Get these valid data types from somewhere else
        valid_datatypes = [
            'AlfaNumerico',
            'Documento',
            'Inteiro',
            'Decimal',
            'Moeda',
            'AutoEnumerado',
            'Data/Hora',
            'Data',
            'Hora',
            'Imagem',
            'Som',
            'Video',
            'URL',
            'Verdadeiro/Falso',
            'Texto',
            'Arquivo',
            'HTML',
            'Email',
            'JSON'
        ]
        return valid_datatypes

    @property
    def datatype(self):
        return self._datatype

    @datatype.setter
    def datatype(self, t):
        """
        Check if is a valid datatype
        """
        if t in self.valid_types():
            self._datatype = t
        else:
            msg = 'TypeError Wrong tipo. The value you supllied for tipo is not valid: %s' % t
            raise Exception(msg)
            self._datatype = None

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
    def multivalued(self, m):
        """
        Check if is a valid multivalued
        """
        if isinstance(m, bool):
            self._multivalued = m
        else:
            msg = 'TypeError Wrong multivalued. The value you supllied for multivalued is not valid: %s' % m
            raise Exception(msg)
            self._multivalued = None

class Required():
    """
    Define valid required
    """
    def __init__(self, required):
        self.required = required

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, r):
        """
        Check if is a valid required
        """
        if isinstance(r, bool):
            self._required= r
        else:
            msg = 'TypeError Wrong required. The value you supllied for required is not valid: %s' % r
            raise Exception(msg)
            self._required = None
