#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'carlos'

from liblightbase import lbutils
from liblightbase.lbutils.conv import dict2document
from liblightbase.lbutils.const import PYSTR

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

    def __init__(self, select=['*'], order_by=OrderBy(),
            literal='', limit=10, offset=0, distinct=None):
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

        if distinct is not None:
            self.distinct = distinct

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
        assert isinstance(value, PYSTR), msg
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
        if not value == None:
            msg = "limit property must be a int"
            assert isinstance(value, PYSTR), msg
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

class LBFile(object):
        def __init__(self, id_file=None, id_doc=None, filename=None, filesize=None, \
                mimetype=None, filetext=None, dt_ext_text=None, download=None):
            self.id_file = id_file
            self.id_doc = id_doc
            self.filename = filename
            self.filesize = filesize
            self.mimetype = mimetype
            self.filetext = filetext
            self.dt_ext_text = dt_ext_text
            self.download = download

class FileResults(list):

    def __init__(self, results):
        results_object = [LBFile(**dictobj) for dictobj in results]
        super(FileResults, self).__init__(results_object)

class NullDocument(object):
    pass

class Results(list):

    def __init__(self, base, results):
        results_object = [dict2document(base, dictobj) \
            if dictobj is not None else NullDocument() for dictobj in results]
        super(Results, self).__init__(results_object)

class FileCollection(object):

    def __init__(self, results, result_count, limit, offset):

        # @property results:
        self.results = FileResults(results)

        # @property result_count:
        self.result_count = result_count

        # @property limit:
        self.limit = limit

        # @property offset:
        self.offset = offset

class Collection(object):

    def __init__(self, base, results, result_count, limit, offset):

        # @property results:
        self.results = Results(base, results)

        # @property result_count:
        self.result_count = result_count

        # @property limit:
        self.limit = limit

        # @property offset:
        self.offset = offset
