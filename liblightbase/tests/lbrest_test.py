#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase import lbrest

from liblightbase.tests import lbjson_test


class LBRestTestCase(lbjson_test.TestJSON):
    """
    Test LBGenerator communication library
    """
    def setUp(self):
        """
        Load data from previous tests
        :return:
        """

        # Start base definition
        lbjson_test.TestJSON.setUp(self)
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

        self.base = Base(
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
        # End Base definition

        self.rest_url = "http://localhost/api"
        self.rest = lbrest.LBRest(rest_url=self.rest_url)
        pass

    def test_rest_communication(self):
        """
        Test REST communication
        :return:
        """
        response = self.rest.send_request(method='get')
        assert response.status_code == 200

    def test_base_creation(self):
        """
        Test REST base creation
        :return:
        """
        response = self.rest.create_base(self.base.json)
        assert response.status_code == 200

    def test_base_removal(self):
        """
        Rest base removal from REST
        :return:
        """
        response = self.rest.remove_base(self.base.metadata.name)
        assert response.status_code == 200

    def tearDown(self):
        """
        Remove data from all tests
        :return:
        """
        lbjson_test.TestJSON.tearDown(self)

        pass