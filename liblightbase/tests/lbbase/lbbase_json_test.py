
import unittest
from liblightbase.lbbase.__init__2 import Base
from liblightbase.lbbase.fields import *
import os.path
import json
from liblightbase.lbbase.conversion import json_to_base

class JSONTestCase(unittest.TestCase):
    """
    Unity tests for Base
    """
    def setUp(self):
        """
        Set up test data
        """
        index1 = Index('Textual')
        index2 = Index('Ordenado')

        nome_pessoa = Field(
            name='nome',
            description='Esse é o nome da pessoa',
            datatype = DataType('Documento'),
            indices = [index1],
            multivalued = Multivalued(False)
        )

        cpf_pessoa = Field(
            name='cpf',
            description='Esse é o CPF da pessoa',
            datatype = DataType('Inteiro'),
            indices = [index1, index2],
            multivalued = Multivalued(False)
        )

        nome_dep = Field(
            name='nome',
            description='Esse é o nome do dependente',
            datatype = DataType('Documento'),
            indices = [index1],
            multivalued = Multivalued(False)
        )

        nasc_dep = Field(
            name='datanascimento',
            description='Essa é a data de nascimento do dependente',
            datatype = DataType('Documento'),
            indices = [index1],
            multivalued = Multivalued(False)
        )

        dependentes = Group(
            name='dependentes',
            description='Dependentes da pessoa',
            content = [nome_dep, nasc_dep],
            multivalued = Multivalued(True)
        )

        self.base = Base(
            name='Pessoa',
            description='Base que armazena informações de pessoas',
            content = [nome_pessoa, cpf_pessoa, dependentes]
        )

        self.base_file = os.path.join(os.path.join(os.path.dirname(__file__), 'static'), 'base.json')

    def test_create(self):
        """ Test base JSON creation
        """
        base_json = self.base.json

        # Write it to a test file
        fd = open('/tmp/json_base.json', 'w+')
        fd.write(str(base_json))
        fd.close()

    def test_parse_self(self):
        """ Test receiving an JSON object and parse it to a base object
        """
        base_json = self.base.json
        base = json_to_base(base_json)

    def test_parse_file(self):
        """
        Test opening a test multivalued JSON file and creating an object
        """
        # Open JSON file
        f = open(self.base_file)
        base_json = f.read()

        # Parse it as a base
        base = json_to_base(base_json)

    def tearDown(self):
        """
        Remove test data
        """
        pass

