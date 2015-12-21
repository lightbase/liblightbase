# -*- coding: utf-8 -*-

from liblightbase.lbrest.core import LBRest
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils.const import PYSTR
from liblightbase.lbutils.conv import json2base

class BaseREST(LBRest):

    """
    """

    def __init__(self, rest_url, response_object=False):
        """
        @param rest_url:
        @param basename:
        """
        super(BaseREST, self).__init__(rest_url, response_object)

    def search(self, search_obj='{}'):
        """
        @param search_obj:
        """
        return self.send_request(self.httpget,
            data={self.search_param: search_obj})

    # delete path - get(self, base)
    def get(self, base):
        """
        @param name: base's name
        """
        if isinstance(base, Base):
            basename = base.metadata.name
        else:
            msg = 'Base must be Base object or string.'
            assert isinstance(base, PYSTR), msg
            basename = base
        response = self.send_request(self.httpget,
            url_path=[basename])
        return json2base(response)

    def create(self, base):
        """
        @param base:
        """
        return self.send_request(self.httppost,
            data={self.base_param: base.json})

    # delete path - update(self, base)
    def update(self, base):
        """
        @param base:
        """
        return self.send_request(self.httpput,
            url_path=[base.metadata.name],
            data={self.base_param: base.json})

    def delete(self, base):
        """
        @param base:
        """
        if isinstance(base, Base):
            basename = base.metadata.name
        else:
            msg = 'Base must be Base object or string.'
            assert isinstance(base, PYSTR), msg
            basename = base.metadata.name
        return self.send_request(self.httpdelete,
            url_path=[basename])
