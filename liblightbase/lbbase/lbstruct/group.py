# -*- coding: utf-8 -*-
import voluptuous
from liblightbase.lbbase.lbstruct.properties import Multivalued
from liblightbase.lbbase.const import RESERVED_STRUCT_NAMES
from liblightbase import lbutils
import liblightbase.lbbase.content

class GroupMetadata(object):

    """
    The group metadata is all data related to the group. The main purpose of 
    metadata is to facilitate in the discovery of relevant information, more 
    often classified as resource discovery.
    """

    # @property _namemaxlen: The maximum number of characters allowed in the
    # name property.
    #_namemaxlen = 5000

    # @property _aliasmaxlen: The maximum number of characters allowed in the
    # alias property.
    #_aliasmaxlen = 5000

    # @property _descmaxlen: The maximum number of characters allowed in the
    # description property.
    #_descmaxlen = 5000

    def __init__(self, name, alias, description, multivalued):

        # @param name: The group name should obey the rules: 
        # No identifier can contain ASCII NUL (0x00) or a byte with a value of
        # 255. Database, table, and column names should not end with space  
        # characters. Database and table names cannot contain “/”, “\”, “.”, or 
        # characters that are not allowed in file names.
        self.name = name

        # @param alias: The group alias is a nickname for the group. It has no 
        # restriction of characters and is used for a better (human) 
        # identification of the group.
        self.alias = alias

        # @param description: Exposition, argumentation, or narration of the 
        # group existing purpose.
        self.description = description

        # @param multivalued: The multivalued property is a tipical type of 
        # NoSQL and multidimensional database. Indicates the structure capacity 
        # of holding more than one value.
        self.multivalued = Multivalued(multivalued)

    @property
    def name(self):
        """ @property name getter
        """
        return self._name

    @name.setter
    def name(self, value):
        """ @property name setter
        """
        try:
            assert(isinstance(value, str))
        except AssertionError:
            # Check for valid unicode strings
            try:
                assert(isinstance(value,unicode))
            except:
                raise ValueError('Invalid chars on name. It must be an ascii string')
        #try:
        #    assert(len(value) <= self._namemaxlen)
        #except AssertionError:
        #    raise ValueError('Group name %s max length must be %i!' % (value,
        #        self._namemaxlen))
        try:

            msg = 'Group name %s is a reserved name. Please use another name.'\
                % value
            assert value not in RESERVED_STRUCT_NAMES

            #msg = 'Group name %s max length must be %i!' % (value,
            #    self._namemaxlen)
            #assert len(value) <= self._namemaxlen

            msg = 'Group name %s must contains ascii characters\
                only!' % value
            assert all(ord(c) < 128 for c in value)

        except AssertionError:
            raise ValueError(msg)
        else:
            self._name = value.lower()

    @property
    def alias(self):
        """ @property alias getter
        """
        return self._alias

    @alias.setter
    def alias(self, value):
        """ @property alias setter
        """
        try:
            assert(isinstance(value, str))
        except AssertionError:
            # Check for valid unicode strings
            try:
                assert(isinstance(value,unicode))
            except:
                raise ValueError('Invalid chars on alias. It must be an ascii string')
        #try:
        #    assert(len(value) <= self._aliasmaxlen)
        #except AssertionError:
        #    raise ValueError('Group alias %s max length must be %i!' % (value,
        #        self._aliasmaxlen))

        self._alias = value

    @property
    def description(self):
        """ @property description getter
        """
        return self._description

    @description.setter
    def description(self, value):
        """ @property description setter
        """
        if not isinstance(value,str):
            if not isinstance(value,unicode):
                raise ValueError('Description must be string or unicode!')
        #try:
        #    assert(len(value) <= self._descmaxlen)
        #except AssertionError:
        #    raise ValueError('Description max length is %i!' % self._descmaxlen)

        self._description= value

    @property
    def multivalued(self):
        """ @property multivalued getter
        """
        return self._multivalued.multivalued

    @multivalued.setter
    def multivalued(self, value):
        """ @property multivalued setter
        """
        try:
            assert(isinstance(value, Multivalued))
        except AssertionError:
            raise ValueError('This should be an instance of Multivalued. \
                Instead it is %s' % value)
        else:
            self._multivalued = value

    @property
    def asdict(self):
        """ @property asdict: Dictonary format of group metadata model.
        """
        return {
            'name': self.name,
            'alias': self.alias,
            'description': self.description,
            'multivalued': self.multivalued
        }

    @property
    def json(self):
        """ @property json: JSON format of group metadata model.
        """
        return lbutils.object2json(self.asdict)

class Group():
    """
    The group structure holds collection of structures. The group structure has 
    the same model than the base, containing metadata and content properties.
    """

    is_group = True
    is_field = False

    def __init__(self, metadata, content):

        # @param metadata: The group metadata is all data related to the group.
        # The main purpose of metadata is to facilitate in the discovery of 
        # relevant information, more often classified as resource discovery.
        self.metadata = metadata

        # @param content: The group content is a list of structures that compose
        # the group schema. Structures may also have metadata and content, giving
        # the group a recursive modeling.
        self.content = content

    @property
    def metadata(self):
        """ @property metadata getter
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """ @property metadata setter
        """
        try:
            assert isinstance(value, GroupMetadata)
        except AssertionError:
            raise ValueError('Group metadata must be of type GroupMetadata \
            instead of %s' % value)
        else:
            self._metadata = value

    @property
    def content(self):
        """ @property content getter
        """
        return self._content

    @content.setter
    def content(self, value):
        """ @property content setter
        """
        try:
            assert isinstance(value, liblightbase.lbbase.content.Content)
        except AssertionError:
            raise ValueError('Group content must be of type Content \
            instead of %s' % value)
            assert len(value) > 0, 'Group content must have at least one \
                structure.'
        except AssertionError as e:
            raise ValueError(' '.join(str(e).split()))
        else:
            self._content = value

    def schema(self, base, id):
        """ 
        A database schema is a collection of meta-data that describes the 
        relations in a database. A schema can be simply described as the
        "layout" of a database or the blueprint that outlines the way data is 
        organized into tables. This method build the group schema, returning it.
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
        """
        The document model is a template of the inherent structure in document.
        This method builds the document model, returning it.
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

    @property
    def asdict(self):
        """ @property asdict: Dictonary format of base model. 
        """
        return {
            'group': {
                'metadata': self.metadata.asdict,
                'content': self.content.asdict
            }
        }

    @property
    def json(self):
        """ @property json: JSON format of group model. 
        """
        return lbutils.object2json(self.asdict)


