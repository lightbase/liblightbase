
import collections
from liblightbase.lbbase import fields
from liblightbase import lbutils
from liblightbase.lbregistry import Registry
import json
import voluptuous

class Base():
    """
    Defining a LB Base object
    """


    def __init__(self, name, description, password, color, content,
                index_export=False , index_url=None, index_time=None,
                doc_extract=False, extract_time=None):
        """
        Base attributes
        """
        self.name = name
        self.description = description
        self.password = password
        self.color = color
        self.content = content
        self.index_export = index_export
        self.index_url = index_url
        self.index_time = index_time
        self.doc_extract = doc_extract
        self.extract_time = extract_time

        self.__docs__ = { }
        self.__reldata__ = { }

    @property
    def index_export(self):
        return self._index_export

    @index_export.setter
    def index_export(self, ie):
        if isinstance(ie, bool):
            self._index_export = ie
        else:
            raise ValueError('index_export value must be boolean!')

    @property
    def index_url(self):
        return self._index_url

    @index_url.setter
    def index_url(self, url):
        if self.index_export:
            _url = lbutils.validate_url(url)
            if len(_url.split('/')) is not 5:
                raise Exception("""
                    index_url must have the following format:
                    http://host:port/index_name/type_name
                    But received: %s
                """ % str(url))
            self._index_url = _url
        else:
            self._index_url = url

    @property
    def index_time(self):
        return self._index_time

    @index_time.setter
    def index_time(self, it):
        if self.index_export:
            if isinstance(it, int):
                self._index_time = it
            else:
                raise ValueError('index_time value must be integer!')
        else:
            self._index_time = it

    @property
    def doc_extract(self):
        return self._doc_extract

    @doc_extract.setter
    def doc_extract(self, de):
        if isinstance(de, bool):
            self._doc_extract = de
        else:
            raise ValueError('doc_extract value must be boolean!')

    @property
    def extract_time(self):
        return self._extract_time

    @extract_time.setter
    def extract_time(self, et):
        if self.doc_extract:
            if isinstance(et, int):
                self._extract_time = et
            else:
                raise ValueError('extract_time value must be integer!')
        else:
            self._extract_time = et

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, c):

        content_list = [ ]
        self.__names__ = [ ]

        if type(c) is list:
            for value in c:

                if isinstance(value, fields.Field):
                    self.__names__.append(value.name)

                elif isinstance(value, fields.Group):
                    self.__names__.append(value.name)
                    self.__names__ = self.__names__ + value.__names__
                else:
                    msg = 'InstanceError This should be an instance of Field or Group. instead it is %s' % value
                    raise Exception(msg)

                content_list.append(value)

            repeated_names = [x for x, y in collections.Counter(self.__names__).items() if y > 1]
            if len(repeated_names) > 0:
                raise Exception('Base cannot have repeated names : %s' % str(repeated_names))

            self._content = content_list
        else:
            msg = 'Type Error: content must be a list instead of %s' % c
            raise Exception(msg)
            self._content = None

    @property
    def object(self):
        """ Builds base object 
        """
        return dict(
            metadata = dict(
                name = self.name,
                description = self.description,
                password = self.password,
                color = self.color,
                index_export = self.index_export,
                index_url = self.index_url,
                index_time = self.index_time,
                doc_extract = self.doc_extract,
                extract_time = self.extract_time
            ),
            content = [attr.object for attr in self.content]
        )

    def validate(self, registry, _meta):
        """ Validate registry, given id
        """
        id = _meta.id_reg

        # Create docs memory area
        self.__docs__[id] = [ ]
        self.__reldata__[id] = { }

        # Delete metadata from registry
        if '_metadata' in registry: del registry['_metadata']

        # Build schema
        _schema = self.schema(id)
        try:
            # Validates registry
            registry = _schema(registry)
        except Exception as e:
            # If process goes wrong, clear the docs memory area
            del self.__docs__[id]
            del self.__reldata__[id]
            raise Exception('Registry data is not according to base definition. Details: %s' % str(e))

        # Put registry metadata back
        registry['_metadata'] = _meta.__dict__

        return registry, self.__reldata__[id], self.__docs__[id]

    def schema(self, id):
        """ Builds base Schema
        """
        _schema = dict()
        for attr in self.content:
            required = getattr(attr, 'required', False)
            name = attr.name
            if required:
                name = voluptuous.Required(attr.name)
            _schema.update({ name: attr.schema(self, id) })
        return voluptuous.Schema(_schema)

    @property
    def reg_model(self):
        """ Builds registry model
        """
        _schema = { attr.name: attr.reg_model(self) for attr in self.content }
        Encoder = type('Encoder', (json.JSONEncoder,), {'default': lambda self, o: o._encoded()})
        return json.dumps(_schema, cls=Encoder, ensure_ascii=False)

    @property
    def json(self):
        """ Builds base JSON
        """
        return json.dumps(self.object, ensure_ascii=False)

    def get_path(self, registry, path):
        """ Get value from given path in registry
        """
        registry = Registry(self, registry)
        return registry.get_path(path)

    def set_path(self, registry, path, value):
        """ Set value from given path in registry
        """
        registry = Registry(self, registry)
        return registry.set_path(path, value)

    def put_path(self, registry, path, value):
        """ Put value from given path in registry
        """
        registry = Registry(self, registry)
        return registry.put_path(path, value)

    def delete_path(self, registry, path):
        """ Delete value from given path in registry
        """
        registry = Registry(self, registry)
        return registry.delete_path(path)

    @property
    def relational_fields(self):
        """ Get relational fields
        """
        rel_fields = { }

        for struct in self.content:
            if isinstance(struct, fields.Field) and struct.is_rel:
                rel_fields[struct.name] = struct
            elif isinstance(struct, fields.Group):
                rel_fields.update(struct.relational_fields)

        return rel_fields
