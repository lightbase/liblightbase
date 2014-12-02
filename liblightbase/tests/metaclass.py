import liblightbase
from liblightbase import lbutils
from liblightbase.lbutils.conv import json2base
from liblightbase.lbutils.conv import document2json
from liblightbase.lbutils.conv import document2dict
from liblightbase.lbutils.conv import json2document
from liblightbase.lbutils.conv import dict2document

import unittest

class LBDocumentTestCase(unittest.TestCase):
    """
    Test base metaclasses 
    """

    def setUp(self):
        """
        Load data from previous tests and setup test data
        :return:
        """
        #lbjson_test.TestJSON.setUp(self)

        self.json_base = '''{
            "metadata":
                {
                    "id_base": 5,
                    "dt_base": "10/05/2014 10:21:49",
                    "file_ext": false,
                    "idx_exp": false,
                    "idx_exp_url": "",
                    "idx_exp_time": "0",
                    "file_ext_time": "0",
                    "name": "pessoa",
                    "description": "qqqqqqq",
                    "password": "qqqqqqqq",
                    "color": ""
                },
            "content": [
                {
                    "field": {
                        "name": "nome",
                        "alias": "c5",
                        "description": "efdewf",
                        "datatype": "Text",
                        "required": true,
                        "multivalued": false,
                        "indices": [
                            "Textual"
                        ]
                    }
                },
                {
                    "field": {
                        "name": "carros",
                        "alias": "",
                        "description": "",
                        "datatype": "Text",
                        "required":true,
                        "multivalued": true,
                        "indices": [
                            "Textual"
                        ]
                    }
                },
                {
                    "group": {
                        "metadata": {
                            "name": "dependente",
                            "alias": "c3",
                            "description": "yrjt",
                            "multivalued": true
                        },
                        "content": [
                            {
                                "group": {
                                    "metadata": {
                                        "name": "gmulti",
                                        "alias": "c3",
                                        "description": "yrjt",
                                        "multivalued": true
                                    },
                                    "content": [
                                        {
                                            "field": {
                                                "name": "teste",
                                                "alias": "c1",
                                                "description": "gtrgtr",
                                                "datatype": "Text",
                                                "required": false,
                                                "multivalued": false,
                                                "indices": [
                                                    "Textual"
                                                ]
                                            }
                                        },
                                        {
                                            "field": {
                                                "name": "teste2",
                                                "alias": "t2",
                                                "description": "gtrgtr",
                                                "datatype": "Text",
                                                "required": false,
                                                "multivalued": true,
                                                "indices": [
                                                    "Textual"
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "field": {
                                    "name": "nome_dep",
                                    "alias": "c1",
                                    "description": "gtrgtr",
                                    "datatype": "Text",
                                    "required": true,
                                    "multivalued":false,
                                    "indices": [
                                        "Textual"
                                    ]
                                }
                            },
                            {
                                "field": {
                                    "name": "idade_dep",
                                    "alias": "c2",
                                    "description": "rgregetg",
                                    "datatype": "Integer",
                                    "required": false,
                                    "multivalued": false,
                                    "indices": [
                                        "Textual"
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }'''

        self.base = json2base(self.json_base)

    def test_create_metaclasses(self):
        for struct in self.base.__allstructs__:
           MetaClass = self.base.get_struct(struct)._metaclass(self.base)

    def test_create_document(self):

        Dependente = self.base.metaclass('dependente')
        Gmulti = self.base.metaclass('gmulti')
        Pessoa = self.base.metaclass()

        pessoa = Pessoa(
            nome='Antony',
            dependente=[
                Dependente(
                    nome_dep='Neymar',
                    idade_dep=12,
                    gmulti=[
                        Gmulti(
                            teste='False'
                        ),
                        Gmulti(
                            teste='False'
                        )
                    ]
                )
            ],
            carros=['x', 'y', 'z'],
        )

    def test_json2document(self):
        pessoa1 = {
            'nome': 'Antony',
            'dependente': [
                {
                    'nome_dep': 'Neymar',
                    'idade_dep': 12,
                    'gmulti': [
                        {
                            'teste' : 'False'
                        },
                        {
                            'teste' : 'False'
                        }
                    ]
                },
            ],
            'carros': ['x', 'y', 'z'],
        }

        pessoa2 = dict2document(self.base, pessoa1)

        assert pessoa2.nome == pessoa1['nome']
        assert pessoa2.carros == pessoa1['carros']
        assert pessoa2.dependente[0].nome_dep == pessoa1['dependente'][0]['nome_dep']
        assert pessoa2.dependente[0].gmulti[0].teste == pessoa1['dependente'][0]['gmulti'][0]['teste']
        assert pessoa2.dependente[0].idade_dep == pessoa1['dependente'][0]['idade_dep']

    def test_document2json(self):
        pessoa1 = {
            'nome': 'Antony',
            'dependente': [
                {
                    'nome_dep': 'Neymar',
                    'idade_dep': 12,
                    'gmulti': [
                        {
                            'teste' : 'False'
                        },
                        {
                            'teste' : 'False'
                        }
                    ]
                },
            ],
            'carros': ['x', 'y', 'z'],
        }
        pessoa1 = lbutils.object2json(pessoa1)

        pessoa2 = json2document(self.base, pessoa1)
        #Gmulti = self.base.metaclass('gmulti')
        #Gmulti.teste= True
        #pessoa2.dependente.gmulti[1] = Gmulti() 
        #pessoa2.dependente.gmulti.append(55)
        j = document2json(self.base, pessoa2, indent=4)

        fd = open('/tmp/document.json', 'w+')
        fd.write(j)
        fd.close()

    def test_x(self):
        Pessoa = self.base.metaclass()
        Gmulti = self.base.metaclass('gmulti')
        Dependente = self.base.metaclass('dependente')
        lbbase = self.base

        class Y(Gmulti):

            @property
            def teste(self):
                return Gmulti.teste.__get__(self)

            @teste.setter
            def teste(self, v):
                Gmulti.teste.__set__(self, v)

        class X(Pessoa):

            def __init__(self, **args):
                super(X, self).__init__(**args)
            
            @property
            def nome(self):
                return Pessoa.nome.__get__(self)

            @nome.setter
            def nome(self, v):
                Pessoa.nome.__set__(self, v)

            @property
            def dependente(self):
                return Pessoa.dependente.__get__(self)

            @dependente.setter
            def dependente(self, v):
                Pessoa.dependente.__set__(self, v)

            def set_dependentes(self):
                g1 = dict(
                    teste='ww',
                    teste2=[
                        'dgfkdsgsghslkdghsk',
                        'dsgjsd.,gjsd.gjs'
                    ]
                )
                g1_obj = dict2document(lbbase, g1, Gmulti)
                g2 = dict(
                    teste='ww',
                    teste2=[
                        'dgfkdsgsghslkdghsk',
                        'dsgjsd.,gjsd.gjs'
                    ]
                )
                g2_obj = dict2document(lbbase, g2, Gmulti)
                g3 = dict(
                    teste='ww',
                    teste2=[
                        'dgfkdsgsghslkdghsk',
                        'dsgjsd.,gjsd.gjs'
                    ]
                )
                g3_obj = dict2document(lbbase, g3, Gmulti)
                g4 = dict(
                    teste='ww',
                    teste2=[
                        'dgfkdsgsghslkdghsk',
                        'dsgjsd.,gjsd.gjs'
                    ]
                )
                g4_obj = dict2document(lbbase, g4, Gmulti)
                d1 = dict(
                    nome_dep='xxx',
                    gmulti=[g1, g2]
                )
                d1_obj = dict2document(lbbase, d1, Dependente)
                d2 = dict(
                    nome_dep='xxx',
                    gmulti=[g3, g4]
                )

                d2_obj = dict2document(lbbase, d2, Dependente)

                d1 = [
                    d1_obj,
                    d2_obj
                ]
                self.dependente = d1
        
        x = X(nome='aa', carros=['d'])
        x.set_dependentes()
        j = document2json(self.base, x, indent=4)
        self.assertIsNotNone(j)
        fd = open('/tmp/document2.json', 'w+')
        fd.write(j)
        fd.close()

        p = document2dict(self.base, x)
        y = X(**p)
        self.assertIsInstance(y, X)
