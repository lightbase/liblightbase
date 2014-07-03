import unittest

from liblightbase.lbbase.__init__2 import Base
from liblightbase.lbbase.fields import *
from liblightbase.lbbase.conversion import json_to_base

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

    def test_datatype(self):
        """
        Try to setup Tipo object
        """
        datatype = DataType('Inteiro'),

    def test_field(self):
        """
        Try to setup a field object
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')

        field = Field(
            name = 'nome',
            description = 'Esse é o nome da pessoa',
            datatype = DataType('Inteiro'),
            indices = [index1, index2],
            multivalued = Multivalued(False),
            required = Required(False)
        )

    def test_group(self):
        """
        Try to setup group
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')
        field1 = Field(
            name = 'field1',
            description = 'desc1',
            datatype = DataType('Inteiro'),
            indices = [index1, index2],
            multivalued = Multivalued(False),
            required = Required(False)
        )

        field2 = Field(
            name = 'field2',
            description = 'desc2',
            datatype = DataType('Documento'),
            indices = [index1],
            multivalued = Multivalued(True),
            required = Required(True)
        )

        group = Group(
            name = 'group2',
            description = 'groupdesc2',
            content = [field1, field2],
            multivalued = Multivalued(False)
        )

    def test_base(self):
        """
        Test base object creation
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')
        field1 = Field(
            name = 'field1',
            description = 'desc1',
            datatype = DataType('Inteiro'),
            indices = [index1, index2],
            multivalued = Multivalued(False),
            required = Required(True)
        )

        field2 = Field(
            name = 'field2',
            description = 'desc2',
            datatype = DataType('Documento'),
            indices = [index1],
            multivalued = Multivalued(True),
            required = Required(True)
        )

        group2 = Group(
            name = 'group2',
            description = 'groupdesc2',
            content = [field1, field2],
            multivalued = Multivalued(False)
        )

        group1 = Group(
            name = 'group1',
            description = 'groupdesc1',
            content = [field1, field2, group2],
            multivalued = Multivalued(True)
        )

        base = Base(
            name = 'base1',
            description = 'base1 description',
            index_export = 'index_export',
            index_url = 'index_url',
            index_time = 'index_time',
            doc_extract = 'doc_extract',
            extract_time = 'extract_time',
            content = [group1, field1, field2]
        )
        print(base.json)

    def tearDown(self):
        """
        Remove test data
        """
        pass

