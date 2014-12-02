#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'carlos'

from liblightbase.lbutils.const import PYSTR

class PathOperation():
    """
    Class model representing operations with path.
    """

    def __init__(self, path, mode, fn=None, args=[]):
        """
        :param path:
        :param mode:
        :param fn:
        :param args:
        :return:
        """

        #property path:
        self.path = path

        #property mode:
        self.mode = mode

        #property fn:
        self.fn = fn

        #property args:
        self.args = args

    @property
    def path(self):
        """
        @property path getter
        """
        return self._path

    @path.setter
    def path(self, value):
        """
        @property path setter
        """
        msg = "path property must be a string"
        assert isinstance(value, PYSTR), msg
        self._path = value

    @property
    def mode(self):
        """
        @property mode getter
        """
        return self._mode

    @mode.setter
    def mode(self, value):
        """
        @property mode setter
        :param value:
        :return:
        """
        msg = "mode property must be a string"
        assert isinstance(value, PYSTR), msg

        msg2 = "mode property must be in the list of operations"
        assert value in ["insert", "update", "delete"], msg2

        self._mode = value

    @property
    def fn(self):
        """
        @property fn getter
        :return:
        """
        return self._fn

    @fn.setter
    def fn(self, value):
        """
        @property fn setter
        :param value:
        :return:
 0        """
        if not value == None:
            msg = "fn property must be a string"
            assert isinstance(value, PYSTR), msg

    @property
    def args(self):
        """
        @property args getter
        :return:
        """
        return self._args

    @args.setter
    def args(self, value):
        """
        @property args setter
        :param value:
        :return:
        """
        msg = "args property must be list."
        assert isinstance(value, list), msg
        self._args = value