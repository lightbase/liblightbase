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


        self.json_base =  '''{"metadata":{"id_base":5,"dt_base":"10/05/2014 10:21:49","file_ext":false,"idx_exp":false,"idx_exp_url":"","idx_exp_time":"0","file_ext_time":"0","name":"pessoa","description":"qqqqqqq","password":"qqqqqqqq","color":""},"content":[{"field":{"name":"nome","alias":"c5","description":"efdewf","datatype":"Text","required":true,"multivalued":false,"indices":["Textual"]}},{"field":{"name":"carros","alias":"","description":"","datatype":"Text","required":true,"multivalued":true,"indices":["Textual"]}},{"group":{"metadata":{"name":"dependente","alias":"c3","description":"yrjt","multivalued":false},"content":[{"group":{"metadata":{"name":"gmulti","alias":"c3","description":"yrjt","multivalued":true},"content":[{"field":{"name":"teste","alias":"c1","description":"gtrgtr","datatype":"Text","required":false,"multivalued":false,"indices":["Textual"]}}]}},{"field":{"name":"nome_dep","alias":"c1","description":"gtrgtr","datatype":"Text","required":true,"multivalued":false,"indices":["Textual"]}},{"field":{"name":"idade_dep","alias":"c2","description":"rgregetg","datatype":"Integer","required":false,"multivalued":false,"indices":["Textual"]}}]}}]}'''

        self.base = json2base(self.json_base)

    def test_create_metaclasses(self):
        for struct in self.base.__allstructs__:
           MetaClass = self.base.get_struct(struct)._metaclass(self.base)

    def test_create_document(self):

        Dependente = self.base.metaclass('dependente')
        Gmulti = self.base.metaclass('gmulti')
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
                        'teste' : 'True'
                    }
                ]
           },
           'carros' : ['x', 'y', 'z'],
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

        class Y(Gmulti):

            @property
            def teste(self):
                return Gmulti.teste.__get__(self)

            @teste.setter
            def teste(self, v):
                Gmulti.teste.__set__(self, v)
        
        g1 = Y(teste='ww')
        d1 = Dependente(nome_dep='xxx', gmulti=[g1])
        x = X(nome='aa', carros=['d'], dependente=d1)
        x2 = X(nome=5, carros=['d'])
        j = document2json(self.base, x, indent=4)
        print(x.nome)
        print(x2.nome)
        raise Exception(j)





