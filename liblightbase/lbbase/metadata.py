import datetime
from liblightbase import lbutils

class BaseMetadata(object):
    """ Defining a LB Base Metadata Object
    """

    _namemaxlen = 5000
    _descmaxlen = 5000

    def __init__(self, name=None, description=None, password=None, color=None,
        model=None, dt_base=None, id_base=None, idx_exp=False , idx_exp_url=None,
        idx_exp_time=5, file_ext=False, file_ext_time=5):

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

        self.asdict = {
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
            'file_ext_time': self.file_ext_time
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
            raise ValueError('Base name value must be string!')
        try:
            assert(len(value) <= self._namemaxlen)
        except AssertionError:
            raise ValueError('Base name %s max length must be %i!' % (value,
                self._namemaxlen))
        try:
            # check ascii characters
            assert all(ord(c) < 128 for c in value)
        except AssertionError:
            raise ValueError('''Base name %s must contains ascii characters
                only!''' % value)
        else:
            self._name = value.lower()

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
    def id_base(self):
        return self._id_base

    @id_base.setter
    def id_base(self, value):
        try:
            assert(isinstance(value, int))
        except AssertionError:
            raise ValueError('id_base value must be integer!')
        else:
            self._id_base = value

    @property
    def dt_base(self):
        return self._dt_base

    @dt_base.setter
    def dt_base(self, value):
        if isinstance(value, datetime.datetime):
            self._dt_base = value
        elif value is None:
            # Default to now
            self._dt_base = datetime.datetime.now()
        else:
            try:
                value = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                raise ValueError('dt_base value must be instance of datetime! \
                    or str in the format %d/%m/%Y %H:%M:%S. Instead it is {}'\
                    .format(value))
            else:
                self._dt_base = value

    @property
    def idx_exp(self):
        return self._idx_exp

    @idx_exp.setter
    def idx_exp(self, value):
        try:
            assert(isinstance(value, bool))
        except AssertionError:
            raise ValueError('idx_exp value must be boolean!')
        else:
            self._idx_exp = value

    @property
    def idx_exp_url(self):
        return self._idx_exp_url

    @idx_exp_url.setter
    def idx_exp_url(self, value):
        assert(type(value) is str or type(value) is type(None))
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
        return self._idx_exp_time

    @idx_exp_time.setter
    def idx_exp_time(self, value):
        if value is None:
            # Default to 300 seconds
            self._idx_exp_time = 300
        else:
            try:
                value = int(value)
                assert(isinstance(value, int))
            except AssertionError:
                raise ValueError('idx_exp_time value must be integer!')
            else:
                self._idx_exp_time = value

    @property
    def file_ext(self):
        return self._file_ext

    @file_ext.setter
    def file_ext(self, value):
        if value is None:
            # Default to true
            self._file_ext = True
        else:
            try:
                assert(isinstance(value, bool))
            except AssertionError:
                raise ValueError('file_ext value must be boolean!')
            else:
                self._file_ext = value

    @property
    def file_ext_time(self):
        return self._file_ext_time

    @file_ext_time.setter
    def file_ext_time(self, value):
        if value is None:
            # Default to 300 seconds
            self._file_ext_time=300
        else:
            try:
                value = int(value)
                assert(isinstance(value, int))
            except AssertionError:
                raise ValueError('file_ext_time value must be integer!')
            else:
                self._file_ext_time = value

    def _encoded(self):
        """

        :return: Return object JSON
        """

        return self.asdict