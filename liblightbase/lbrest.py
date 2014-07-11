#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
#import urlparse

from requests.exceptions import HTTPError


SESSION_COOKIES = None

class LBRest(object):
    """
    Liblightbase Rest communication
    """
    def __init__(self, rest_url):
        self.rest_url = rest_url

    def to_url(self, *args):
        """ Make a list of args and join "/" between list elements
        """
        args = [arg for arg in args if arg is not None]
        return '/'.join(args)

    @property
    def cookies(self):
        session_cookies = getattr(self, '_cookies', None)
        if not session_cookies:
            self._cookies = SESSION_COOKIES
        return self._cookies

    @cookies.setter
    def cookies(self, c):
        self._cookies = c
        globals()['SESSION_COOKIES'] = c

    def send_request(self, method, url='', **kwargs):
        """
        Tries to return json response, raise RequestError if exception occurs.
        """
        # First get request method
        request_method = getattr(requests, method)
        # Make http request
        full_url = self.rest_url + self.to_url('', url)
        response = request_method(full_url, cookies=self.cookies, **kwargs)
        try:
            # Check if request has gone wrong
            response.raise_for_status()
            # Everything is alright, return response
            return response
        except HTTPError:
            # Something got wrong, raise error
            raise RequestError(response.text)

    def create_base(self, base):
        """
        Create a base on REST
        """
        request_data = {'json_base': base.json}
        response = self.send_request(method='post', data=request_data)

        return response

    def remove_base(self, base):
        """
        Remove a base on REST
        """
        request_data = {'json_base': base.json}
        base_name = base.metadata.name
        response = self.send_request(method='delete', url=base_name, data=request_data)

        return response




class RequestError(Exception):
    """
    TODO: Manage REST exceptions
    """
    pass