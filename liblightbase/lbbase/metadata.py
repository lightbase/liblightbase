import datetime
from liblightbase import lbutils
from liblightbase.lbutils.const import PYSTR

class BaseMetadata(object):
    """ 
    The base metadata is all data related to the base. The main purpose of 
    metadata is to facilitate in the discovery of relevant information, more 
    often classified as resource discovery.
    """

    def __init__(self, name=None, description='', password='', color='',
        model=None, dt_base=None, id_base=0, idx_exp=False , idx_exp_url='',
        idx_exp_time=300, file_ext=False, file_ext_time=300, txt_mapping=''):

        """ Base Metadata Attributes
        """

        # @param name: The base name. Should accept only low-case characters
        # separated by underscore. Also should be a unique constraint, to ensure
        # all bases names will be unique.
        self.name = name

        # @param description: The base longer description.
        self.description = description

        # @param id_base: The primary key for this table and uniquely identify
        # each base in the table.
        self.id_base = id_base

        # @param dt_base: The base creation date (date and time). 
        self.dt_base = dt_base

        # @param password: The base password. Used for permission purposes.
        self.password = password

        # @param color: The base color. Have to remove this. 
        self.color = color

        # @param idx_exp: Index exportaction. Flag used to indicate if the base
        # needs to be indexed. Each document inserted on Base will be indexed if
        # this flag is true. The index engine is external to this API.
        self.idx_exp = idx_exp

        # @param idx_exp_url: Index exportaction URI (Uniform Resource Locator).
        # Identifier used to index the documents. Accepted format is:
        # http://<IP>:<PORT>/<INDEX>/<TYPE>. If @param idx_exp is true, when
        # inserting a document to base, a HTTP request is sent to this URI.
        self.idx_exp_url = idx_exp_url

        # @param idx_exp_time: Index exportaction time. Time in seconds used by 
        # asynchronous indexer to sleep beetwen the indexing processes.
        self.idx_exp_time = idx_exp_time

        # @param file_ext: File extraction. Flag used by asynchronous text 
        # extractor. Indicates the need of extracting the text of the base files.
        self.file_ext = file_ext

        # @param file_ext_time: File extraction time. Time in seconds used by 
        # asynchronous extractor to sleep beetwen the extracting processes.
        self.file_ext_time = file_ext_time

        # @param txt_mapping: .
        self.txt_mapping = txt_mapping

    @property
    def name(self):
        """ @property name getter
        """
        return self._name

    @name.setter
    def name(self, value):
        """ @property name setter
        """
        msg = 'Invalid chars on Base name. It must be an ascii string'
        assert(isinstance(value, PYSTR)), msg
        # check ascii characters
        assert all(ord(c) < 128 for c in value), msg
        self._name = str(value).lower()

    @property
    def description(self):
        """ @property description getter
        """
        return self._description

    @description.setter
    def description(self, value):
        """ @property description setter
        """
        msg = 'Base description must be string or unicode!'
        assert(isinstance(value, PYSTR)), msg
        self._description= value

    @property
    def id_base(self):
        """ @property id_base getter
        """
        return self._id_base

    @id_base.setter
    def id_base(self, value):
        """ @property id_base setter
        """
        msg = 'id_base value must be integer!'
        assert(isinstance(value, int)), msg
        self._id_base = value

    @property
    def dt_base(self):
        """ @property id_base getter
        """
        return self._dt_base

    @dt_base.setter
    def dt_base(self, value):
        """ @property id_base setter
        """
        if isinstance(value, datetime.datetime):
            self._dt_base = value
        elif value is None:
            # Default to now
            self._dt_base = datetime.datetime.now()
        else:
            try:
                value = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                raise ValueError('dt_base value must be instance of datetime'+\
                    ' or str in the format %d/%m/%Y %H:%M:%S. Instead it is {}'\
                    .format(value))
            else:
                self._dt_base = value

    @property
    def idx_exp(self):
        """ @property idx_exp getter
        """
        return self._idx_exp

    @idx_exp.setter
    def idx_exp(self, value):
        """ @property idx_exp setter
        """
        try:
            assert(isinstance(value, bool))
        except AssertionError:
            raise ValueError('idx_exp value must be boolean!')
        else:
            self._idx_exp = value

    @property
    def idx_exp_url(self):
        """ @property idx_exp_url getter
        """
        return self._idx_exp_url

    @idx_exp_url.setter
    def idx_exp_url(self, value):
        """ @property idx_exp_url setter
        """
        if value is not None:
            assert isinstance(value, PYSTR)
        if self.idx_exp:
            url = lbutils.validate_url(value)
            if len(url.split('/')) is not 5:
                raise ValueError('''idx_exp_url must have the following format:
                    http://host:port/index_name/type_name But received: %s''' %
                    str(url))
            self._idx_exp_url = value
        else:
            self._idx_exp_url = value

    @property
    def idx_exp_time(self):
        """ @property idx_exp_time getter
        """
        return self._idx_exp_time

    @idx_exp_time.setter
    def idx_exp_time(self, value):
        if value is None:
            # Default to 300 seconds
            self._idx_exp_time = 300
        else:
            try:
                value = int(value)
            except ValueError:
                raise ValueError('idx_exp_time value must be integer!')
            else:
                self._idx_exp_time = value

    @property
    def file_ext(self):
        """ @property file_ext getter
        """
        return self._file_ext

    @file_ext.setter
    def file_ext(self, value):
        if value is None:
            # Default to false 
            self._file_ext = False
        else:
            msg = 'file_ext value must be boolean!'
            assert isinstance(value, bool), msg
            self._file_ext = value

    @property
    def file_ext_time(self):
        """ @property file_ext_time getter
        """
        return self._file_ext_time

    @file_ext_time.setter
    def file_ext_time(self, value):
        """ @property file_ext_time setter
        """
        if value is None:
            # Default to 300 seconds
            self._file_ext_time=300
        else:
            try:
                value = int(value)
            except ValueError:
                raise ValueError('file_ext_time value must be integer!')
            else:
                self._file_ext_time = value

    @property
    def asdict(self):
        """ @property asdict: Dictonary format of base metadata model. 
        """
        return {
            'name': self.name,
            'description': self.description,
            'id_base': self.id_base,
            'dt_base': self.dt_base,
            'password': self.password,
            'color': self.color,
            'idx_exp': self.idx_exp,
            'idx_exp_url': self.idx_exp_url,
            'idx_exp_time': self.idx_exp_time,
            'file_ext': self.file_ext,
            'file_ext_time': self.file_ext_time,
            'txt_mapping': self.txt_mapping
        }

    @property
    def json(self):
        """ @property json: JSON format of base metadata model. 
        """
        return lbutils.object2json(self.asdict)
