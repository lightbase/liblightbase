
from liblightbase.lbbase.metadata import BaseMetadata
from liblightbase.lbbase.content import Content
from liblightbase import lbtypes
from liblightbase import lbutils
from liblightbase.lbdocument import Tree
import voluptuous

class Base():

    """ Defining a Base Object
    """

    def __init__(self, metadata, content):

        # @param metadata: 
        self.metadata = metadata

        # @param content: 
        self.content = content

        # @property __files__: 
        self.__files__ = { }

        # @property __cfiles__: 
        self.__cfiles__ = { }

        # @property __reldata__: 
        self.__reldata__ = { }

        metadata_dict= self.metadata.asdict
        content_dict = self.content.asdict
        metadata_dict['model'] = self.document_model

        # @property json: 
        self.asdict = {
            'metadata': metadata_dict,
            'content': content_dict,
        }

        self.json = lbutils.object2json(self.asdict)

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        try:
            assert isinstance(value, BaseMetadata)
        except AssertionError:
            raise ValueError('Base metadata must be of type BaseMetadata \
                instead of %s' % value)
        else:
            self._metadata = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        try:
            assert isinstance(value, Content)
        except AssertionError:
            raise ValueError('Base content must be of type Content \
            instead of %s' % value)
        else:
            self._content = value

    def validate(self, document, _meta):
        """ Validate document, given id
        """
        id = _meta.id_doc

        # Create docs memory area
        self.__files__[id] = [ ]
        self.__cfiles__[id] = [ ]
        self.__reldata__[id] = { }

        # Delete metadata from document
        if '_metadata' in document: del document['_metadata']

        # Build schema
        _schema = self.schema(id)
        try:
            # Validates document
            document = _schema(document)
        except Exception as e:
            # If process goes wrong, clear the docs memory area
            del self.__files__[id]
            del self.__cfiles__[id]
            del self.__reldata__[id]
            raise Exception('document data is not according to base definition. \
                Details: %s' % str(e))

        # Put document metadata back
        document['_metadata'] = _meta.__dict__

        return (document,
               self.__reldata__[id],
               self.__files__[id],
               self.__cfiles__[id])

    def schema(self, id):
        """ Builds base Schema
        """
        schema = dict()
        for struct in self.content:
            if struct.is_field:
                structname = struct.name
            elif struct.is_group:
                structname = struct.metadata.name
            if getattr(struct, 'required', False):
                structname = voluptuous.Required(structname)
            schema.update({structname: struct.schema(self, id)})
        return voluptuous.Schema(schema)

    def get_struct(self, sname):
        """ @param sname: structure name to find
            @return: Field or Group 
            This method return the structure corresponding to @sname.
        """
        try:
            return self.__structs__[sname]
        except KeyError:
            raise KeyError("Field %s doesn't exist on base definition." % sname)

    @property
    def document_model(self):
        """ Builds document model
        """
        model = { }
        for struct in self.content:
            if struct.is_field:
                model[struct.name] = struct.document_model(self)
            else:
                model[struct.metadata.name] = struct.document_model(self)
        return model

    def get_path(self, document, path):
        """ Get value from given path in document
        """
        return Tree(document, self).get_path(path)

    def set_path(self, document, path, value):
        """ Set value from given path in document
        """
        index, document = Tree(document, self, True).set_path(path, value)
        return index, document.todict()

    def put_path(self, document, path, value):
        """ Put value from given path in document
        """
        return Tree(document, self, True).put_path(path, value).todict()

    def delete_path(self, document, path):
        """ Delete value from given path in document
        """
        return Tree(document, self).delete_path(path).todict()

    @property
    def relational_fields(self):
        """ Get relational structures 
        """
        rel_fields = { }

        for struct in self.content:
            if struct.is_field and struct.is_rel:
                rel_fields[struct.name] = struct
            elif struct.is_group:
                rel_fields.update(struct.relational_fields)

        return rel_fields
