#!/usr/env python
# -*- coding: utf-8 -*-

import unittest
from liblightbase.lbbase import Base
from liblightbase.lbbase.fields import *
import os.path
from liblightbase.lbbase.genesis import json_to_base

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
            alias='alias',
            description='Esse é o nome da pessoa',
            datatype = DataType('Document'),
            indices = [index1],
            multivalued = False,
            required = Required(True)
        )

        cpf_pessoa = Field(
            name='cpf',
            alias='alias',
            description='Esse é o CPF da pessoa',
            datatype = DataType('Integer'),
            indices = [index1, index2],
            multivalued = False,
            required = Required(True)
        )

        nome_dep = Field(
            name='nome',
            alias='alias',
            description='Esse é o nome do dependente',
            datatype = DataType('Document'),
            indices = [index1],
            multivalued=False,
            required = Required(True)
        )

        nasc_dep = Field(
            name='datanascimento',
            alias='alias',
            description='Essa é a data de nascimento do dependente',
            datatype = DataType('Document'),
            indices = [index1],
            multivalued=False,
            required = Required(True)
        )

        dependentes = Group(
            name='dependentes',
            alias='alias',
            description='Dependentes da pessoa',
            content = [nome_dep, nasc_dep],
            multivalued = Multivalued(True)
        )

        self.base = Base(
            name='Pessoa',
            description='Base que armazena informações de pessoas',
            password='123456',
            idx_exp =False,
            idx_exp_url = 'index_url',
            idx_exp_time = 'index_time',
            file_ext = 'doc_extract',
            file_ext_time = 'extract_time',
            color='#FFFFFF',
            content = [nome_pessoa, cpf_pessoa, dependentes]
        )

        self.base_file = os.path.join(os.path.join(os.path.dirname(__file__), 'static'), 'base.json')

    def test_create_file(self):
        """ Test base JSON creation
        """
        base_json = self.base.json
        print(base_json)

        # Write it to a test file
        fd = open('/tmp/json_base.json', 'w+')
        fd.write(str(base_json))
        fd.close()

        assert os.path.isfile('/tmp/json_base.json')

    def test_parse_self(self):
        """ Test receiving an JSON object and parse it to a base object
        """
        base_json = self.base.json
        base = json_to_base(base_json)

        assert isinstance(base, Base)

    def test_parse_file(self):
        """
        Test opening a test multivalued JSON file and creating an object
        """
        # Open JSON file
        f = open(self.base_file)
        base_json = f.read()

        # Parse it as a base
        base = json_to_base(base_json)

        assert isinstance(base, Base)

    def tearDown(self):
        """
        Remove test data
        """
        pass