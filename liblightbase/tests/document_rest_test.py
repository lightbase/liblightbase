
import liblightbase
from liblightbase import lbutils
from liblightbase import lbbase
from liblightbase.lbutils.conv import json2base
from liblightbase.lbutils.conv import document2json
from liblightbase.lbutils.conv import document2dict
from liblightbase.lbutils.conv import json2document
from liblightbase.lbutils.conv import dict2document
import datetime
import json

from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST


import unittest

class DocumentRESTTest(unittest.TestCase):
    """
    Test base metaclasses 
    """

    def setUp(self):
        """
        Load data from previous tests and setup test data
        :return:
        """
        #lbjson_test.TestJSON.setUp(self)

        rest_url = 'http://api.brlight.net/api'
        self.base_rest = BaseREST(rest_url)
        self.base = self.base_rest.get('expedido')
        self.doc_rest = DocumentREST(rest_url, self.base)

    def test_get_doc(self):
        document = self.doc_rest.get(1)

        document_type = self.base.metaclass()
        assert isinstance(document, document_type)

        with open('/tmp/document.json', 'w+') as f:
            f.write(document2json(self.base, document))







