#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import unittest

from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content


class TestJSON(unittest.TestCase):
    """
    Test JSON conversion for objects
    """
    def setUp(self):
        """
        Load test data
        :return:
        """

        pass


    def test_json_fields(self):
        """
        Test JSON fields serialization
        :return:
        """
        index1 = 'Textual'
        index2 = 'Ordenado'
        datatype = 'Integer'

        field = Field(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            alias='alias',
            datatype = datatype,
            indices = [index1, index2],
            multivalued = False,
            required = False
        )
        j = field.json
        print(j)
        assert j

    def test_json_groups(self):
        """
        Test JSON grups serialization
        :return:
        """
        index1 = 'Textual'
        index2 = 'Ordenado'
        datatype = 'Integer'

        field = Field(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            alias='alias',
            datatype = datatype,
            indices = [index1, index2],
            multivalued = False,
            required = False
        )

        field2 = Field(
            name = 'field2',
            alias='alias',
            description = 'desc2',
            datatype = 'Document',
            indices = [index1],
            multivalued = True,
            required = True
        )

        content_list = Content()
        content_list.append(field)
        content_list.append(field2)

        group = Group(
            metadata=GroupMetadata(
                name = 'group2',
                alias='alias',
                description = 'groupdesc2',
                multivalued =False
            ),
            content=content_list,
        )

        j = group.json
        print(j)
        assert j

    def test_json_base(self):
        """
        Test JSON base serialization
        :return:
        """
        index1 = 'Textual'
        index2 = 'Ordenado'
        datatype = 'Integer'

        field = Field(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            alias='alias',
            datatype = datatype,
            indices = [index1, index2],
            multivalued = False,
            required = False
        )

        field2 = Field(
            name = 'field2',
            alias='alias',
            description = 'desc2',
            datatype = 'Document',
            indices = [index1],
            multivalued = True,
            required = True
        )

        content_list = Content()
        content_list.append(field)
        content_list.append(field2)

        group = Group(
            metadata=GroupMetadata(
                name = 'group2',
                alias='alias',
                description = 'groupdesc2',
                multivalued =False
            ),
            content=content_list,
        )

        content_list = Content()
        content_list.append(group)
        content_list.append(field)
        content_list.append(field2)

        base = Base(
            metadata=BaseMetadata(
                id_base=1,
                name = 'base1',
                description = 'base1 description',
                password='123456',
                idx_exp =False,
                idx_exp_url = 'index_url',
                idx_exp_time=300,
                file_ext=True,
                file_ext_time=300,
                color='#FFFFFF',
            ),
            content=content_list
        )

        j = base.json
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