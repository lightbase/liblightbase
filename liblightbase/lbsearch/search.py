from liblightbase import lbutils

class OrderBy(object):
    """ 
    The ORDER BY keyword sorts the records in ascending order by default.
    To sort the records in a descending order, you can use the DESC keyword.
    To sort the records in a ascending order, you can use the ASC keyword.
    """

    def __init__(self, asc = [], desc = []):
        """ OrderBy constructor
        """
        # @property asc: list with structure names
        self.asc = asc

        # @property desc: list with structure names
        self.desc = desc

    @property
    def asc(self):
        """ @property asc getter
        """
        return self._asc

    @asc.setter
    def asc(self, value):
        """ @property asc setter
        """
        msg = 'asc property must be list object.'
        assert isinstance(value, list), msg
        self._asc = value

    @property
    def desc(self):
        """ @property asc getter
        """
        return self._desc

    @desc.setter
    def desc(self, value):
        """ @property asc setter
        """
        msg = 'desc property must be list object.'
        assert isinstance(value, list), msg
        self._desc = value

    def _asjson(self, **kw):
        dict_orderby = {} 
        for key in dir(self):
            if not key[0] == "_":
                dict_orderby[key] = getattr(self, key)
        return lbutils.object2json(dict_orderby)

    def _asdict(self, **kw):
        dict_orderby = {} 
        for key in dir(self):
            if not key[0] == "_":
                dict_orderby[key] = getattr(self, key)
        return dict_orderby

class Search(object):
    """
    """

    def __init__(self, select=[], order_by=OrderBy(),
            literal='', limit=10, offset=10):
        """
        """
        # @property select:
        self.select = select

        # @property order_by:
        self.order_by = order_by

        # @property literal:
        self.literal = literal

        # @property limit:
        self.limit = limit

        # @property offset:
        self.offset = offset

    def _asjson(self, **kw):
        dict_search = {} 
        for key in dir(self):
            if not key[0] == "_":
                if isinstance(getattr(self, key), OrderBy):
                    value = getattr(self, key)._asdict()
                else:
                    value = getattr(self, key)
                dict_search[key] = value 
        return lbutils.object2json(dict_search)

    def _asdict(self, **kw):
        dict_search = {} 
        for key in dir(self):
            if not key[0] == "_":
                if isinstance(getattr(self, key), OrderBy):
                    value = getattr(self, key)._asdict()
                else:
                    value = getattr(self, key)
                dict_search[key] = value 
        return  dict_search

    @property
    def select(self):
        """@property select getter
        """
        return self._select

    @select.setter
    def select(self, value):
        """@property select setter
        """
        msg = 'select property must be list object.'
        assert isinstance(value, list), msg
        self._select = value

    @property
    def order_by(self):
        """@property order_by getter
        """
        return self._order_by

    @order_by.setter
    def order_by(self, value):
        """@property order_by setter
        """
        msg = "order_by propert mut be a OrderBy instance"
        assert isinstance(value, OrderBy), msg
        self._order_by = value

    @property
    def literal(self):
        """@property literal getter
        """
        return self._literal

    @literal.setter
    def literal(self, value):
        """@property literal setter
        """
        msg = "literal property must be a string"
        assert isinstance(value, str), msg
        self._literal = value

    @property
    def limit(self):
        """@property limit getter
        """
        return self._limit

    @limit.setter
    def limit(self, value):
        """@property limit setter
        """
        msg = "limit property must be a int"
        assert isinstance(value, int), msg
        self._limit = value

    @property
    def offset(self):
        """@property offset getter
        """
        return self._offset

    @offset.setter
    def offset(self, value):
        """@property offset setter
        """
        msg = "offset property must be a int"
        assert isinstance(value, int), msg
        self._offset = value