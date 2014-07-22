import liblightbase
from liblightbase import lbutils
from liblightbase import lbbase
from liblightbase.lbbase import genesis
from liblightbase.lbconv import document2json
from liblightbase.lbconv import document2dict
from liblightbase.lbconv import json2document
from liblightbase.lbconv import dict2document
import datetime
import json

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


        self.json_base =  '''{"metadata":{"id_base":5,"dt_base":"10/05/2014 10:21:49","file_ext":false,"idx_exp":false,"idx_exp_url":"","idx_exp_time":"0","file_ext_time":"0","name":"pessoa","description":"qqqqqqq","password":"qqqqqqqq","color":""},"content":[{"field":{"name":"nome","alias":"c5","description":"efdewf","datatype":"Text","required":true,"multivalued":false,"indices":["Textual"]}},{"field":{"name":"carros","alias":"","description":"","datatype":"Text","required":true,"multivalued":true,"indices":["Textual"]}},{"group":{"metadata":{"name":"dependente","alias":"c3","description":"yrjt","multivalued":false},"content":[{"group":{"metadata":{"name":"gmulti","alias":"c3","description":"yrjt","multivalued":true},"content":[{"field":{"name":"teste","alias":"c1","description":"gtrgtr","datatype":"Text","required":false,"multivalued":false,"indices":["Textual"]}}]}},{"field":{"name":"nome_dep","alias":"c1","description":"gtrgtr","datatype":"Text","required":true,"multivalued":false,"indices":["Textual"]}},{"field":{"name":"idade_dep","alias":"c2","description":"rgregetg","datatype":"Integer","required":false,"multivalued":false,"indices":["Textual"]}}]}}]}'''

        self.base = genesis.json_to_base(json.loads(self.json_base))

    def test_create_metaclasses(self):
        for struct in self.base.__allstructs__:
           MetaClass = self.base.get_struct(struct).metaclass(self.base, 0)

    def test_create_document(self):

        Dependente = self.base.get_metaclass('dependente')
        Gmulti = self.base.get_metaclass('gmulti')
        Pessoa = self.base.metaclass()

        pessoa = Pessoa(
            nome = 'Antony',
            dependente = Dependente(
                nome_dep = 'Neymar',
                idade_dep = 12,
                gmulti = [
                    Gmulti(
                        teste = 'False'
                    ),
                    Gmulti(
                        teste = 'False'
                    )
                ]
           ),
           carros = ['x', 'y', 'z'],
        )

    def test_json2document(self):

        pessoa1 = {
           'nome' : 'Antony',
            'dependente' : {
                'nome_dep' : 'Neymar',
                'idade_dep': 12,
                'gmulti' : [
                    {
                        'teste' : 'False'
                    },
                    {
                        'teste' : 'False'
                    }
                ]
           },
           'carros' : ['x', 'y', 'z'],
        }

        pessoa2 = dict2document(self.base, pessoa1)

        assert pessoa2.nome == pessoa1['nome']
        assert pessoa2.carros == pessoa1['carros']
        assert pessoa2.dependente.nome_dep == pessoa1['dependente']['nome_dep']
        assert pessoa2.dependente.gmulti[0].teste == pessoa1['dependente']['gmulti'][0]['teste']
        assert pessoa2.dependente.idade_dep == pessoa1['dependente']['idade_dep']



    def test_document2json(self):
        pessoa1 = {
           'nome' : 'Antony',
            'dependente' : {
                'nome_dep' : 'Neymar',
                'idade_dep': 12,
                'gmulti' : [
                    {
                        'teste' : 'False'
                    },
                    {
                        'teste' : 'False'
                    }
                ]
           },
           'carros' : ['x', 'y', 'z'],
        }
        pessoa1 = lbutils.object2json(pessoa1)

        pessoa2 = json2document(self.base, pessoa1)
        j = document2json(self.base, pessoa2, indent=4)

        fd = open('/tmp/document.json', 'w+')
        fd.write(j)
        fd.close()





