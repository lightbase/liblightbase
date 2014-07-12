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
        Load data from previous tests and setup test data
        :return:
        """
        lbjson_test.TestJSON.setUp(self)

        # Start base definition
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

        self.base = Base(
            metadata=base_metadata,
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
        response = self.rest.create_base(self.base)
        assert response.status_code == 200

    def test_base_removal(self):
        """
        Rest base removal from REST
        :return:
        """
        response = self.rest.remove_base(self.base)
        assert response.status_code == 200
        pass

    def tearDown(self):
        """
        Remove data from all tests
        :return:
        """
        lbjson_test.TestJSON.tearDown(self)

        pass
