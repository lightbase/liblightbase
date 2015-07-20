# -*- coding: utf-8 -*-  
import requests
from requests.exceptions import HTTPError
from liblightbase import lbutils
from liblightbase.lbbase.struct import Base

SESSION_COOKIES = None

class LBRest(object):

    """
    Liblightbase Rest communication
    """

    # @httpverb properties:
    httpget = 'GET'
    httppost = 'POST'
    httpput = 'PUT'
    httpdelete = 'DELETE'

    # @property doc_prefix:
    doc_prefix = 'doc'

    # @property file_prefix:
    file_prefix = 'file'

    # @property base_param:
    base_param = 'json_base'

    # @property doc_param:
    doc_param = 'value'

    # @property doc_param:
    file_param = 'file'

    # @property search_param:
    search_param = '$$'

    # @property path_param:
    path_param = 'path'

    def __init__(self, rest_url, response_object=False):
        self.rest_url = rest_url
        self.response_object = response_object

    def to_url(self, *args):
        """ Make a list of args and join "/" between list elements
        """
        args = [arg for arg in args if arg is not None]
        return '/'.join(args)

    @property
    def cookies(self):
        """
        """
        session_cookies = getattr(self, '_cookies', None)
        if not session_cookies:
            self._cookies = SESSION_COOKIES
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        """
        """
        self._cookies = value
        globals()['SESSION_COOKIES'] = value

    def send_request(self, method, url_path=[ ], **kwargs):
        """
        @param method:
        @param path:
        Tries to return json response, raise RequestError if exception occurs.
        """
        # First get request method
        request_method = getattr(requests, method.lower())
        # Make http request
        full_url = self.to_url(self.rest_url, *url_path)
        response = request_method(full_url, cookies=self.cookies, **kwargs)
        if self.response_object:
            # Return response object for application level error handling
            return response
        try:
            # Check if request has gone wrong
            response.raise_for_status()
        except HTTPError:
            # Something got wrong, raise error
            raise HTTPError(response.text)
        else:
            # Everything is alright, return response
            return response.text

    @property
    def base(self):
        """ @property base getter
        """
        return self._base

    @base.setter
    def base(self, value):
        """ @property base setter
        """
        if isinstance(value, Base):
            self.basename = value.metadata.name
        elif isinstance(value, str):
            self.basename = value
        else:
            raise TypeError('base must be a Base object or a string.')
        self._base = value
