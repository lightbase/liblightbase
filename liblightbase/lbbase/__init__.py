
from liblightbase.lbbase import fields
from liblightbase import lbutils
from liblightbase.lbregistry import Registry
import json
import voluptuous

class Base():
    """
    Defining a LB Base object
    """

    __docs__ = { }

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
        content_list = list()
        if type(c) is list:
            for value in c:
                if isinstance(value, fields.Field) or isinstance(value, fields.Group):
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

    def validate(self, registry, id):
        """ Validate registry, given id
        """
        # Ensures id is integer
        _coerce = lbutils.Coerce(int)
        id = _coerce(id)

        # Create docs memory area
        self.__docs__[id] = [ ]

        # Delete id from registry
        if 'id_reg' in registry: del registry['id_reg']

        # Build schema
        _schema = self.schema(id)
        try:
            registry = _schema(registry)
        except Exception as e:
            # If process goes wrong, clear the docs memory area
            del self.__docs__[id]
            raise Exception('Registry data is not according to base definition. Details: %s' % str(e))

        # Put registry id back
        registry['id_reg'] = id
        return json.dumps(registry, ensure_ascii=False)

    def schema(self, id):
        """ Builds base Schema
        """
        _schema = dict()
        for attr in self.content:
            required = getattr(attr, 'required', None)
            name = attr.name
            if required:
                if required.required is True:
                    name = voluptuous.Required(attr.name)
            _schema.update({ name: attr.schema(self, id) })
        return voluptuous.Schema(_schema)

    @property
    def reg_model(self):
        """ Builds registry model
        """
        _schema = { attr.name: attr.reg_model(self) for attr in self.content }
        Encoder = type('Encoder', (json.JSONEncoder,), {'default': lambda self, o: repr(o)})
        return json.dumps(_schema, cls=Encoder, ensure_ascii=False)

    """
    @property
    def relational_fields(self):
        _relational_fields = dict(
            normal_cols = [ ],
            unique_cols = [ ],
            date_types = [ ],
            Textual = [ ],
            Nenhum = [ ]
        )
        for element in self.content:
            if isinstance(element, fields.Field):
                for index in element.indices:
                    if index.index in ['Ordenado', 'Vazio']:
                        base_cc['normal_cols'].append(fname)
                    if index.index in ['Unico']:
                        base_cc['unique_cols'].append(fname)
                    if index.index in ['Textual']:
                        base_cc['Textual'].append(fname)
                    if index.index in ['Nenhum']:
                        base_cc['Nenhum'].append(fname)
                if field.datatype.datatype == 'Data':
                    base_cc['date_types'].append(fname)

        base.custom_columns = base_cc
    """

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
