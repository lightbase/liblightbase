

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
    def asc(self)
        """ @property asc getter
        """
        return self._asc

    @asc.setter
    def asc(self, value)
        """ @property asc setter
        """
        msg = 'asc property must be list object.'
        assert isinstance(value, list), msg
        self._asc = asc

    @property
    def desc(self)
        """ @property asc getter
        """
        return self._desc

    @desc.setter
    def desc(self, value)
        """ @property asc setter
        """
        msg = 'desc property must be list object.'
        assert isinstance(value, list), msg
        self._desc = desc

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

    def json(self, **kw):

