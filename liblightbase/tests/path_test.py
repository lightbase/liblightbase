#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'carlos'

import unittest
from liblightbase.lbsearch.path import PathOperation


class PathOperationTest(unittest.TestCase):
    """
    Class test PathOperation
    """

    def test_pathoperation(self):
        """
        test pathoperation
        :return:
        """
        path = "path/"
        mode = "insert"
        fn = None
        args = []

        obj = PathOperation(path, mode, fn, args)