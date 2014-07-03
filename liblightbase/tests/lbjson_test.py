#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import unittest
import json

from liblightbase.lbbase import Base
from liblightbase.lbbase.fields import *


class TestJSON(unittest.TestCase):
    """
    Test JSON conversion for objects
    """
    def setUp(self):
        """
        Load test data
        :return:
        """
        self.index1 = Index('Textual')
        index2 = Index('Ordenado')
        self.datatype = DataType('Integer')

        self.field = Field(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            alias='alias',
            datatype = DataType('Integer'),
            indices = [self.index1, index2],
            multivalued = False,
            required = Required(False)
        )

        field2 = Field(
            name = 'field2',
            alias='alias',
            description = 'desc2',
            datatype = DataType('Document'),
            indices = [self.index1],
            multivalued = True,
            required = Required(True)
        )

        self.group = Group(
            name = 'group2',
            alias='alias',
            description = 'groupdesc2',
            content = [self.field, field2],
            multivalued =False
        )

        self.base = Base(
            name = 'base1',
            description = 'base1 description',
            password='123456',
            idx_exp =False,
            idx_exp_url = 'index_url',
            idx_exp_time = 'index_time',
            file_ext = 'doc_extract',
            file_ext_time = 'extract_time',
            color='#FFFFFF',
            content=[self.group, self.field, field2]
        )

        pass

    def test_json_index(self):
        """
        Test JSON index serialization

        :return:
        """

        j = self.index1.json
        assert j

    def test_json_datatypes(self):
        """
        Test JSON dataypes serialization
        :return:
        """
        j = self.datatype.json
        print(j)
        assert j

    def test_json_fields(self):
        """
        Test JSON fields serialization
        :return:
        """
        j = self.field.json
        print(j)
        assert j

    def test_json_groups(self):
        """
        Test JSON grups serialization
        :return:
        """
        j = self.group.json
        assert j

    def test_json_base(self):
        """
        Test JSON base serialization
        :return:
        """
        j = self.base.json
        fd = open('/tmp/test.json', 'w+')
        fd.write(j)
        fd.close()
        assert j

    def tearDown(self):
        """
        Remove test data
        :return:
        """
        pass