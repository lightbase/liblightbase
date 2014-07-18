
from liblightbase.lbbase.metadata import BaseMetadata
from liblightbase.lbbase.content import Content
from liblightbase import lbtypes
from liblightbase import lbutils
from liblightbase.lbdocument import Tree
import voluptuous

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
        self.content = content

        # @property __files__: A dictionary at the format { id_doc: list of 
        # files }. This property helps to identify files contained on each
        # document. When document is submitted, the routine should compare 
        # these files to files present at database, deleting those that aren't
        # present on both lists.
        self.__files__ = { }

        # @property __cfiles__: A dictionary at the format { id_doc: list of 
        # files to be created }. This property contains the new files present
        # in document that do not exist on database yet. The routine should
        # submit these files when submitting document. 
        self.__cfiles__ = { }

        # @property __reldata__: A dictionary at the format {id_doc: {field
        # name: data}}. This property contains the data to be submitted at 
        # relational column at database.
        self.__reldata__ = { }

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
            assert isinstance(value, BaseMetadata)
        except AssertionError:
            raise ValueError('Base metadata must be of type BaseMetadata \
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
            assert isinstance(value, Content), 'Base content must be of type \
                Content instead of %s' % value;
            assert len(value) > 0, 'Base content must have at least one \
                structure.'
        except AssertionError as e:
            raise ValueError(' '.join(str(e).split()))
        else:
            self._content = value

    def validate(self, document, _meta):
        """ Validate document data structure.
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

    @property
    def asdict(self):
        """ @property asdict: Dictionary format of base model.
        """
        metadata_dict= self.metadata.asdict
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

    def metaclass(self):
        """ 
        Generate base metaclass. The base metaclass is an abstraction of 
        document model defined by base structures.
        """
        snames = self.content.__snames__
        rnames = self.content.__rnames__
        basename = self.metadata.name

        class BaseMetaClass(object):
            """ 
            Top-level metaclass. Describes the structures defifined by
            document structure model.
            """

            def __init__(self, **kwargs):
                """ Base metaclass constructor
                """
                a = set(rnames)
                b = set(kwargs.keys())
                if len(a-b) > 0:
                    msg = 'Required key {} not provided'.format(a-b)
                    raise TypeError(msg)

                for arg in kwargs:
                    if arg in snames:
                        setattr(self, arg, kwargs[arg])
                    else:
                        msg = 'Base {} has no structure named {}'\
                            .format(basename, arg)
                        raise AttributeError(msg)

        for struct in self.content:

            # make class properties
            structname, prop = self._make_meta_prop(self, struct)
            setattr(BaseMetaClass, structname, prop)

        BaseMetaClass.__name__ = self.metadata.name
        return BaseMetaClass

    def _make_meta_prop(self, base, struct):
        """
        Make python's property based on structure attributes.
        @param base: Base object.
        @param struct: Field or Group object.
        """

        # Get structure name.
        if struct.is_field:
            structname = struct.name
        elif struct.is_group:
            structname = struct.metadata.name

        # create "private" attribute name
        attr_name = '_' + structname

        def getter(self):
            """ Property getter
            """
            value = getattr(self, attr_name)
            if struct.is_field:
                return getattr(value, '__value__')
            return value

        def setter(self, value):
            """ Property setter
            """
            struct_metaclass = struct.metaclass(base, id)

            if struct.is_field:
                value = struct_metaclass(value)
            elif struct.is_group:
                if struct.metadata.multivalued:
                    assertion = [isinstance(element,
                        struct_metaclass) for element in value]
                    #assert all(assertion)
                    #'%s should be an instance of %s' % (value, struct_metaclass)
                else:
                    #assert isinstance(value, struct_metaclass), 
                    #'%s should be an instance of %s' % (value, struct_metaclass)
                    pass
            setattr(self, attr_name, value)

        def deleter(self):
            """ Property deleter
            """
            delattr(self, attr_name)

        return structname, property(getter, setter, deleter, structname)

    def json2document(self, document, metaclass=None):
        """
        Build metaclass object given document.
        @param document:
        @param metaclass:
        """

        if metaclass is None:
            metaclass = self.metaclass()

        kwargs = { }
        for member in document:

            struct = self.get_struct(member)

            if struct.is_field:
                kwargs[member] = document[member]

            elif struct.is_group:

                if struct.metadata.multivalued:
                    meta_object = []
                    for element in document[member]:

                        meta_inner_object = self.json2document(
                            document=element,
                            metaclass=struct.metaclass(self, 0)
                        )
                        meta_object.append(meta_inner_object)
                else:
                    meta_object = self.json2document(
                        document=document[member],
                        metaclass=struct.metaclass(self, 0)
                    )

                kwargs[member] = meta_object

        return metaclass(**kwargs)



