#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import unittest
import json

from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbutils.conv import json2base


class TestJSON(unittest.TestCase):
    """
    Test JSON conversion for objects
    """
    def setUp(self):
        """
        Load test data
        :return:
        """
        index1 = 'Textual'
        index2 = 'Ordenado'
        datatype = 'Integer'

        self.field = dict(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            alias='alias',
            datatype = datatype,
            indices = [index1, index2],
            multivalued = False,
            required = False
        )

        self.field2 = dict(
            name = 'field2',
            alias='alias',
            description = 'desc2',
            datatype = 'Document',
            indices = [index1],
            multivalued = True,
            required = True
        )

        self.field3 = dict(
            name = 'field3',
            alias='alias',
            description = 'desc3',
            datatype = 'Text',
            indices = [index1],
            multivalued = False,
            required = True
        )

        self.group_metadata = dict(
            name = 'group2',
            alias='alias',
            description = 'groupdesc2',
            multivalued =False
        )

        self.base_metadata = dict(
            id_base=1,
            name = 'base1',
            description = 'base1 description',
            password='123456',
            idx_exp =False,
            idx_exp_url = 'index_url',
            idx_exp_time=300,
            file_ext=True,
            file_ext_time=300,
            color='#FFFFFF'
        )

        pass


    def test_json_fields(self):
        """
        Test JSON fields serialization
        :return:
        """

        field = Field(**self.field)
        j = field.json
        print(j)
        assert j

    def test_json_groups(self):
        """
        Test JSON groups serialization
        :return:
        """

        field = Field(**self.field)

        field2 = Field(**self.field2)

        content_list = Content()
        content_list.append(field)
        content_list.append(field2)

        group_metadata = GroupMetadata(**self.group_metadata)

        group = Group(
            metadata=group_metadata,
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
        field = Field(**self.field)

        field2 = Field(**self.field2)

        content_list = Content()
        content_list.append(field)
        content_list.append(field2)

        group_metadata = GroupMetadata(**self.group_metadata)

        group = Group(
            metadata=group_metadata,
            content=content_list,
        )

        field3 = Field(**self.field3)

        content_list = Content()
        content_list.append(group)
        content_list.append(field3)

        base_metadata = BaseMetadata(**self.base_metadata)

        base = Base(
            metadata=base_metadata,
            content=content_list
        )

        j = base.json
        fd = open('/tmp/test.json', 'w+')
        fd.write(j)
        fd.close()
        assert j

    def test_base_json(self):
        """
        Test generated JSON conversion back to base
        :return:
        """

        field = Field(**self.field)

        field2 = Field(**self.field2)

        content_list = Content()
        content_list.append(field)
        content_list.append(field2)

        group_metadata = GroupMetadata(**self.group_metadata)

        group = Group(
            metadata=group_metadata,
            content=content_list,
        )

        field3 = Field(**self.field3)

        content_list = Content()
        content_list.append(group)
        content_list.append(field3)

        base_metadata = BaseMetadata(**self.base_metadata)

        base = Base(
            metadata=base_metadata,
            content=content_list
        )

        j = base.json
        b = json2base(j)
        assert(isinstance(b, Base))

    def tearDown(self):
        """
        Remove test data
        :return:
        """
        pass
