#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import urlparse

from requests.exceptions import HTTPError


SESSION_COOKIES = None

class LBRest(object):
    """
    Liblightbase Rest communication
    """
    def __init__(self, rest_url):
        self.rest_url = rest_url

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
        full_url = self.rest_url + url
        print(full_url)
        response = request_method(full_url, cookies=self.cookies, **kwargs)
        try:
            # Check if request has gone wrong
            response.raise_for_status()
            # Everything is alright, return response
            return response
        except HTTPError:
            # Something got wrong, raise error
            raise RequestError(response.text)

    def create_base(self, data):
        """
        Create a base on REST
        """
        response = self.send_request(method='post', data=data)

        return response

    def remove_base(self, base):
        """
        Remove a base on REST
        """
        full_url = '/base/' + base
        response = self.send_request(method='delete', url=full_url)

        return response




class RequestError(Exception):
    """
    TODO: Manage REST exceptions
    """
    pass