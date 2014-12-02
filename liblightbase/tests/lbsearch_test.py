#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'carlos'

import unittest
from liblightbase.lbsearch.search import OrderBy
from liblightbase.lbsearch.search import Search


class ClassSearchTest(unittest.TestCase):
    """Test class search
    """

    def test_Orderby(self):
        """Test class Orderby
        """
        coluna1 = "coluna1"
        coluna2 = "coluna2"
        coluna3 = "coluna3"
        coluna4 = "coluna4"

        OrderBy([coluna1, coluna2], [coluna3, coluna4])

    def test_Search(self):
        """Test class Search
        """
        coluna1 = "coluna1"
        coluna2 = "coluna2"
        coluna3 = "coluna3"
        coluna4 = "coluna4"

        obj_orderby = OrderBy([coluna1, coluna2], [coluna3, coluna4])
        select = ["coluna1", "coluna2"]
        literal = 'select *'
        limit = 10
        offset = 10

        self.obj_Search = Search(select, obj_orderby,
                                 literal, limit, offset)
        self.obj_Search._asjson()