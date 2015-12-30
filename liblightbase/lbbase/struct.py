import voluptuous

from liblightbase import lbutils
from liblightbase.lbutils import exc
from liblightbase.lbbase.content import Content
from liblightbase.lbdoc.doctree import DocumentTree
from liblightbase.lbbase.metadata import BaseMetadata
from liblightbase.lbdoc.metaclass import generate_metaclass
from liblightbase.lbtypes import Matrix


class Base(object):
    """ 
    A base is a set of interrelated data, organized to allow the retrieval 
    of information. A base must provide updated information (structural funds),
    accurate and reliable (not to give the information in half) and according
    to demand (offer what user needs).
    """

    def __init__(self, metadata, content):

        # @param metadata: The base metadata is all data related to the base.
        # The main purpose of metadata is to facilitate in the discovery of 
        # relevant information, more often classified as resource discovery.
        self.metadata = metadata

        # @param content: The base content is a list of structures that compose
        # the base schema. Structures may also have metadata and content, giving
        # the base a recursive modeling.
        # delete path - self.content = content
        self.content = content

        # @property __files__: A dictionary at the format { id_doc: list of 
        # files }. This property helps to identify files contained on each
        # document. When document is submitted, the routine should compare 
        # these files to files present at database, deleting those that aren't
        # present on both lists.
        self.__files__ = { }

        # @property __reldata__: A dictionary at the format {id_doc: {field
        # name: data}}. This property contains the data to be submitted at 
        # relational column at database.
        self.__reldata__ = { }

        # @property __metaclasses__: A dictionary at the format {structname:
        # metaclass}. All metaclasses are created here, so user can acces them
        # to user later, using the @method metaclass().
        self.__metaclasses__ = { }
        self.__rel_fields__ = [ ]

        for structname in self.__allstructs__:
            struct = self.get_struct(structname)
            self.__metaclasses__[structname] = struct._metaclass(self)
            if struct.is_field and (
            'Unico' in struct.indices or 'Ordenado' in struct.indices):
                self.__rel_fields__.append(structname)

        self.__metaclasses__['__base__'] = self._metaclass()

    @property
    def metadata(self):
        """ @property metadata getter
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """ @property metadata setter
        """
        msg = 'Base metadata must be of type BaseMetadata. Instead it is {}'
        assert isinstance(value, BaseMetadata), msg.format(value)
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
        msg = 'Base content must be of type Content. Instead it is {}'
        assert isinstance(value, Content), msg.format(value)
        msg = 'Base content must have at least one structure.'
        assert len(value) > 0, msg
        self._content = value


    def validate(self, document, _meta, validate=True, delete=False):
        """ Validate document data structure.
        """
        id = _meta.id_doc

        if not delete:

            # Para o que serve isso?
            # Create docs memory area
            self.__files__[id] = [ ]
            self.__reldata__[id] = { }

        if not validate:
            for rel_field in self.__rel_fields__:
                self.__reldata__[id][rel_field] = document.get(
                    rel_field, None)
            document['_metadata'] = _meta.__dict__
            return (document,
                   self.__reldata__[id],
                   self.__files__[id],
                   [])

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
            del self.__reldata__[id]
            raise exc.ValidationError(e)

        # Put document metadata back
        document['_metadata'] = _meta.__dict__


        for key, value in document.items():
            if key != '_metadata':
                struct = self.get_struct(key)
                if not value and (isinstance(value, list) or isinstance(value, dict)):
                    self.normalize_reldata(id, struct)
                elif value and (isinstance(value, list) or isinstance(value, dict)):
                    self.check_fields(id, struct, document)

        #self.check_empty_fields(document)

        return (document,
               self.__reldata__[id],
               self.__files__[id],
               [])

    # delete path - schema(self, id)
    def schema(self, id):
        """ 
        A database schema is a collection of meta-data that describes the 
        relations in a database. A schema can be simply described as the
        "layout" of a database or the blueprint that outlines the way data is 
        organized into tables. This method build the base schema, returning it.
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


    def check_fields(self,id, struct, document):
        """ check values in document """
        if struct.is_group:
            for key_field, value_struct in struct.relational_fields.items():
                val = list(self.find(key_field, document))
                if not val:
                    self.normalize_reldata(id, self.get_struct(key_field))


    def normalize_reldata(self, id, struct):
        """
        @document
        """
    #if struct.is_rel:
        if struct.is_field:
            if struct.is_rel:
                #if struct.multivalued:
                #    self.__reldata__[id][struct.name] = Matrix()
                #else:
                #    self.__reldata__[id][struct.name] = None
                if not self.__reldata__.get(id):
                    self.__reldata__[id] = {}
                    self.__reldata__[id][struct.name] = None
                else:
                    self.__reldata__[id][struct.name] = None
        elif struct.is_group:
            for _field in struct.content:
                self.normalize_reldata(id, _field)
                #self.__reldata__[id][_field.name] = None

    def find(self, key, document):
        """Find key in document"""
        if isinstance(document, list):
            for d in document:
                for result in self.find(key, d):
                    yield result

        if isinstance(document, dict):
            for k, v in document.items():
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in self.find(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.find(key, d):
                            yield result


    def get_struct(self, sname):
        """ 
        @param sname: structure name to find
        @return: Field or Group 
        This method return the structure corresponding to @sname.
        """
        try:
            return self.__allstructs__[sname]
        except KeyError:
            raise KeyError("Field %s doesn't exist on base definition." % sname)

    def metaclass(self, sname=None, valreq=True):
        """ 
        @param sname: structure name to find
        This method return the metaclass corresponding to sname.
        """
        if sname is None:
            metaclass = self.__metaclasses__['__base__']
        else:
            try:
                metaclass = self.__metaclasses__[sname]
            except KeyError:
                msg = "Field %s doesn't exist on base definition." % sname
                raise KeyError(msg)
        metaclass.__valreq__ = valreq
        return metaclass

    @property
    def document_model(self):
        """
        The document model is a template of the inherent structure in document.
        This method builds the document model, returning it.
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
        return DocumentTree(document, self).get_path(path)

    def set_path(self, document, path, fn):
        """ Set value from given path in document
        """
        document = DocumentTree(document, self, True).set_path(path, fn)
        return document.todict()

    def put_path(self, document, path, fn):
        """ Put value from given path in document
        """
        return DocumentTree(document, self, True).put_path(path, fn).todict()

    # delete path - delete_path(self, document, path, fn)
    def delete_path(self, document, path, fn):
        """ Delete value from given path in document
        """
        id = document['_metadata']['id_doc']
        for item in path:
            if item == '*' or item.isdigit():
                continue
            struct = self.get_struct(item)
            self.normalize_reldata(id, struct)
        return DocumentTree(document, self).delete_path(path, fn).todict()

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

    @property
    def asdict(self):
        """ @property asdict: Dictionary format of base model.
        """
        metadata_dict = self.metadata.asdict
        content_dict = self.content.asdict
        metadata_dict['model'] = self.document_model
        return {
            'metadata': metadata_dict,
            'content': content_dict,
        }

    @property
    def json(self):
        """ @property json: JSON format of base model.
        """
        return lbutils.object2json(self.asdict)

    @property
    def txt_mapping_json(self):
        """ @property txt_mapping_json: JSON format of txt_mapping.
        """

        '''
        NOTE: Se usarmos "object2json()" será retornado p/ o campo 
        outro valor que não vazio (string vazia) nos casos onde 
        txt_mapping não for enviado! By Questor
        '''
        if self.asdict["metadata"]["txt_mapping"] is not '':
            return lbutils.object2json(self.asdict["metadata"]["txt_mapping"])
        else:
            return self.asdict["metadata"]["txt_mapping"]

    @property
    def __allstructs__(self):
        """ 
        @property __allstructs__: Dictionany at the format {structure name: 
        structure}. Used for quickly access structure by name.
        """
        return self.content.__allstructs__

    @property
    def __allsnames__(self):
        """ 
        @property __allsnames__: List of all structure names. 
        """
        return self.content.__allsnames__

    def _metaclass(self):
        """ 
        Generate base metaclass. The base metaclass is an abstraction of 
        document model defined by base structures.
        """
        self.__files__[0] = [ ]
        self.__reldata__[0] = { }
        return generate_metaclass(self)
