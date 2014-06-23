#!/usr/env python
# -*- coding: utf-8 -*-

import unittest

from liblightbase.lbbase import Base
from liblightbase.lbbase.fields import *

class BaseTestCase(unittest.TestCase):
    """
    Unity tests for Base
    """
    def setUp(self):
        """
        Set up test data
        """
        pass

    def test_index(self):
        """
        Try to setup index value
        """
        index = Index('Vazio')
        assert isinstance(index, Index)

    def test_datatype(self):
        """
        Try to setup Tipo object
        """
        datatype = DataType('Integer')
        assert isinstance(datatype, DataType)

    def test_field(self):
        """
        Try to setup a field object
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')

        field = Field(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            alias='alias',
            datatype = DataType('Integer'),
            indices = [index1, index2],
            multivalued = Multivalued(False),
            required = Required(False)
        )

        assert isinstance(field, Field)

    def test_group(self):
        """
        Try to setup group
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')
        field1 = Field(
            name = 'field1',
            alias='alias',
            description = 'desc1',
            datatype = DataType('Integer'),
            indices = [index1, index2],
            multivalued = Multivalued(False),
            required = Required(False)
        )

        field2 = Field(
            name = 'field2',
            alias='alias',
            description = 'desc2',
            datatype = DataType('Document'),
            indices = [index1],
            multivalued = Multivalued(True),
            required = Required(True)
        )

        group = Group(
            name = 'group2',
            alias='alias',
            description = 'groupdesc2',
            content = [field1, field2],
            multivalued = Multivalued(False)
        )

        assert isinstance(group, Group)

    def test_base(self):
        """
        Test base object creation
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')
        field1 = Field(
            name = 'field1',
            alias='alias',
            description = 'desc1',
            datatype = DataType('Integer'),
            indices = [index1, index2],
            multivalued = Multivalued(False),
            required = Required(True),
        )

        field2 = Field(
            name = 'field2',
            alias='alias',
            description = 'desc2',
            datatype = DataType('Document'),
            indices = [index1],
            multivalued = Multivalued(True),
            required = Required(True)
        )

        group2 = Group(
            name = 'group2',
            alias='alias',
            description = 'groupdesc2',
            content = [field1, field2],
            multivalued = Multivalued(False)
        )

        group1 = Group(
            name = 'group1',
            alias='alias',
            description = 'groupdesc1',
            content = [field1, field2, group2],
            multivalued = Multivalued(True)
        )

        base = Base(
            name = 'base1',
            description = 'base1 description',
            password='123456',
            idx_exp =False,
            idx_exp_url = 'index_url',
            idx_exp_time = 'index_time',
            file_ext = 'doc_extract',
            file_ext_time = 'extract_time',
            color='#FFFFFF',
            content=[group1, field1, field2]
        )

        assert isinstance(base, Base)

    def tearDown(self):
        """
        Remove test data
        """
        pass