#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
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
        lbjson_test.TestJSON.setUp(self)
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
        response = self.rest.remove_base(self.base.name)
        assert response.status_code == 200

    def tearDown(self):
        """
        Remove data from all tests
        :return:
        """
        lbjson_test.TestJSON.tearDown(self)

        pass