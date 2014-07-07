
from liblightbase.lbbase.lbstruct.properties import *
from liblightbase import lbutils

class Field(object):

    """ This is the field description
    """

    is_group = False
    is_field = True

    # String properties max lengths
    _namemaxlen = 5000
    _aliasmaxlen = 5000
    _descmaxlen = 5000

    def __init__(self, name, alias, description, datatype, indices, multivalued,
            required):

        """  Field attributes
        """
        # @param name:
        self.name = name

        # @param alias:
        self.alias = alias

        # @param description:
        self.description = description

        # @param datatype:
        self.datatype = DataType(datatype)

        # @param indices:
        self.indices = [Index(i) for i in indices]

        # @param multivalued:
        self.multivalued = Multivalued(multivalued)

        # @param required:
        self.required = Required(required)

        # @property json:
        self.asdict = {
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

        self.json = lbutils.object2json(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        try:
            assert(isinstance(value, str))
        except AssertionError:
            raise ValueError('Field name value must be string!')
        try:
            assert(len(value) <= self._namemaxlen)
        except AssertionError:
            raise ValueError('Field name %s max length must be %i!' % (value,
                self._namemaxlen))
        try:
            # check ascii characters
            assert all(ord(c) < 128 for c in value)
        except AssertionError:
            raise ValueError('Field name %s must contains ascii characters\
                only!' % value)
        else:
            self._name = value.lower()

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        try:
            assert(isinstance(value, str))
        except AssertionError:
            raise ValueError('Field alias value must be string!')
        try:
            assert(len(value) <= self._aliasmaxlen)
        except AssertionError:
            raise ValueError('Field alias %s max length must be %i!' % (value,
                self._aliasmaxlen))
        else:
            self._alias = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        try:
            assert(isinstance(value, str))
        except AssertionError:
            raise ValueError('Description must be string!')
        try:
            assert(len(value) <= self._descmaxlen)
        except AssertionError:
            raise ValueError('Description max length is %i!' % self._descmaxlen)
        else:
            self._description= value

    @property
    def datatype(self):
        return self._datatype.datatype

    @datatype.setter
    def datatype(self, value):
        try:
            assert isinstance(value, DataType)
        except AssertionError:
            raise ValueError('This must be a instance of datatype. Instead it is\
             %s' % value)
        else:
            self._datatype = value

    @property
    def indices(self):
        return [index.index for index in self._indices]

    @indices.setter
    def indices(self, value):
        if type(value) is not list:
            raise TypeError('indices must be a list instead of %s' % value)
        if all(isinstance(index, Index) for index in value):
            self._indices = value
        else:
            raise ValueError('This should be an instance of Indice. Instead it \
                 is %s' % value)

    @property
    def multivalued(self):
        return self._multivalued.multivalued

    @multivalued.setter
    def multivalued(self, value):
        try:
            assert isinstance(value, Multivalued)
        except AssertionError:
            raise ValueError('This should be an instance of Multivalued. Instead\
                it is %s' % value)
        else:
            self._multivalued = value

    @property
    def required(self):
        return self._required.required

    @required.setter
    def required(self, value):
        try:
            assert isinstance(value, Required)
        except AssertionError:
            raise ValueError('This should be an instance of Required. instead it\
                is %s' % value)
        else:
            self._required = value

    def schema(self, base, id=None):
        """ Builds field schema
        """
        datatype = self._datatype.__schema__

        if self.multivalued is True:
            return [datatype(base, self, id)]
        elif self.multivalued is False:
            return datatype(base, self, id)
        assert False, 'Multivalued property is not True nor False, instead is \
            %s' % self.multivalued

    def document_model(self, base):
        """ Builds registry model
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

    def _encoded(self):
        """
        Return JSON format

        :return:
        """

        return self.asdict