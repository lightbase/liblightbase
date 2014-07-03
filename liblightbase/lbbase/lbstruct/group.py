
import voluptuous
from liblightbase.lbbase.lbstruct.properties import Multivalued
from liblightbase import lbutils

class GroupMetadata():

    _namemaxlen = 5000
    _aliasmaxlen = 5000
    _descmaxlen = 5000

    def __init__(self, name, alias, description, multivalued):

        # @param name:
        self.name = name

        # @param alias:
        self.alias = alias

        # @param description:
        self.description = description

        # @param multivalued:
        self.multivalued = Multivalued(multivalued)

        self.asdict = {
            'name': self.name,
            'alias': self.alias,
            'description': self.description,
            'multivalued': self.multivalued
        }

        self.json = lbutils.object2json(self.asdict)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        try:
            assert(isinstance(value, str))
        except AssertionError:
            raise ValueError('Group name value must be string!')
        try:
            assert(len(value) <= self._namemaxlen)
        except AssertionError:
            raise ValueError('Group name %s max length must be %i!' % (value,
                self._namemaxlen))
        try:
            # check ascii characters
            assert all(ord(c) < 128 for c in value)
        except AssertionError:
            raise ValueError('''Group name %s must contains ascii characters
                only!''' % value)
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
            raise ValueError('Group alias value must be string!')
        try:
            assert(len(value) <= self._aliasmaxlen)
        except AssertionError:
            raise ValueError('Group alias %s max length must be %i!' % (value,
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
    def multivalued(self):
        return self._multivalued.multivalued

    @multivalued.setter
    def multivalued(self, value):
        try:
            assert(isinstance(value, Multivalued))
        except AssertionError:
            raise ValueError('This should be an instance of Multivalued. \
                Instead it is %s' % value)
        else:
            self._multivalued = value

class Group():

    """ This is the group structure definition
    """

    is_group = True
    is_field = False

    def __init__(self, metadata, content):

        # @param metadata:
        self.metadata = metadata

        # @param content:
        self.content = content

        # @property asdict:
        self.asdict = {
            'group': {
                'metadata': self.metadata.asdict,
                'content': self.content.asdict
            }
        }

        # @property json:
        self.json = lbutils.object2json(self.asdict)

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        try:
            assert isinstance(value, GroupMetadata)
        except AssertionError:
            raise ValueError('Group metadata must be of type GroupMetadata \
            instead of %s' % value)
        else:
            self._metadata = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        from liblightbase.lbbase.content import Content
        try:
            assert isinstance(value, Content)
        except AssertionError:
            raise ValueError('Group content must be of type Content \
            instead of %s' % value)
        else:
            self._content = value

    def schema(self, base, id):
        """ Builds base schema
        """
        schema = dict()
        for struct in self.content:
            if struct.is_field:
                structname = struct.name
            elif struct.is_group:
                structname = struct.metadata.name
            if getattr(struct, 'required', False):
                schema[voluptuous.Required(structname)] = struct.schema(base, id)
            else:
                schema[structname] = struct.schema(base, id)
        if self.metadata.multivalued is True:
            return [schema]
        elif self.metadata.multivalued is False:
            return schema

    def document_model(self, base):
        """ Builds document model
        """
        schema = dict()
        for struct in self.content:
            if struct.is_field:
                schema[struct.name] = struct.document_model(base)
            elif struct.is_group:
                schema[struct.metadata.name] = struct.document_model(base)
        if self.metadata.multivalued is True:
            return [schema]
        elif self.metadata.multivalued is False:
            return schema

    @property
    def relational_fields(self):
        """ Get relational fields
        """
        rel_fields = { }

        for struct in self.content:
            if struct.is_field and struct.is_rel:
                rel_fields[struct.name] = struct
            elif struct.is_group:
                rel_fields.update(struct.relational_fields)

        return rel_fields

