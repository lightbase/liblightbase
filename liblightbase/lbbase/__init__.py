
import collections
from liblightbase.lbbase import fields
from liblightbase import lbtypes
from liblightbase import lbutils
from liblightbase.lbdocument import Tree
import voluptuous

class Base():
    """
    Defining a LB Base object
    """


    def __init__(self, name, description, password, color, content,
                dt_base=None, id_base=None,
                idx_exp=False , idx_exp_url=None, idx_exp_time=None,
                file_ext=False, file_ext_time=None):
        """
        Base attributes
        """
        self.id_base = id_base
        self.dt_base = dt_base

        self.name = name
        self.description = description
        self.password = password
        self.color = color
        self.content = content
        self.idx_exp = idx_exp
        self.idx_exp_url = idx_exp_url
        self.idx_exp_time = idx_exp_time
        self.file_ext = file_ext
        self.file_ext_time = file_ext_time

        self.__files__ = { }
        self.__cfiles__ = { }
        self.__reldata__ = { }

    @property
    def idx_exp(self):
        return self._idx_exp

    @idx_exp.setter
    def idx_exp(self, ie):
        if isinstance(ie, bool):
            self._idx_exp = ie
        else:
            raise ValueError('idx_exp value must be boolean!')

    @property
    def idx_exp_url(self):
        return self._idx_exp_url

    @idx_exp_url.setter
    def idx_exp_url(self, url):
        if self.idx_exp:
            _url = lbutils.validate_url(url)
            if len(_url.split('/')) is not 5:
                raise Exception("""
                    idx_exp_url must have the following format:
                    http://host:port/index_name/type_name
                    But received: %s
                """ % str(url))
            self._idx_exp_url = _url
        else:
            self._idx_exp_url = url

    @property
    def idx_exp_time(self):
        return self._idx_exp_time

    @idx_exp_time.setter
    def idx_exp_time(self, it):
        if self.idx_exp:
            if isinstance(it, int):
                self._idx_exp_time = it
            else:
                raise ValueError('idx_exp_time value must be integer!')
        else:
            self._idx_exp_time = it

    @property
    def file_ext(self):
        return self._file_ext

    @file_ext.setter
    def file_ext(self, de):
        if isinstance(de, bool):
            self._file_ext = de
        else:
            raise ValueError('file_ext value must be boolean!')

    @property
    def file_ext_time(self):
        return self._file_ext_time

    @file_ext_time.setter
    def file_ext_time(self, et):
        if self.file_ext:
            if isinstance(et, int):
                self._file_ext_time = et
            else:
                raise ValueError('file_ext_time value must be integer!')
        else:
            self._file_ext_time = et

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
                    msg = 'InstanceError This should be an instance of Field or\
                    Group. instead it is %s' % value
                    raise Exception(msg)

                content_list.append(value)

            repeated_names = [x for x, y in collections.Counter(self.__names__)\
                .items() if y > 1]
            if len(repeated_names) > 0:
                raise Exception('Base cannot have repeated names : %s'
                    % str(repeated_names))

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

                id_base = self.id_base,
                dt_base = self.dt_base,

                name = self.name,
                description = self.description,
                password = self.password,
                color = self.color,
                idx_exp = self.idx_exp,
                idx_exp_url = self.idx_exp_url,
                idx_exp_time = self.idx_exp_time,
                file_ext = self.file_ext,
                file_ext_time = self.file_ext_time,
                model = self.reg_model,
            ),
            content = [attr.object for attr in self.content]
        )

    @property
    def json(self):
        """ Builds base JSON
        """
        return lbutils.object2json(self.object)

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
            raise Exception('document data is not according to base definition. Details: %s' % str(e))

        # Put document metadata back
        document['_metadata'] = _meta.__dict__

        return (document,
               self.__reldata__[id],
               self.__files__[id],
               self.__cfiles__[id])

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
    def reg_model(self):
        """ Builds document model
        """
        return { attr.name: attr.reg_model(self) for attr in self.content }

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
        """ Get relational fields
        """
        rel_fields = { }

        for struct in self.content:
            if isinstance(struct, fields.Field) and struct.is_rel:
                rel_fields[struct.name] = struct
            elif isinstance(struct, fields.Group):
                rel_fields.update(struct.relational_fields)

        return rel_fields
