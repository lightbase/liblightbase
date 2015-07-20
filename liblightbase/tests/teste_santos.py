
import liblightbase
from liblightbase import lbutils
from liblightbase.lbutils.conv import json2base
from liblightbase.lbutils.conv import document2json
from liblightbase.lbutils.conv import document2dict
from liblightbase.lbutils.conv import json2document
from liblightbase.lbutils.conv import dict2document

import unittest


JSON = '''{"metadata":{"file_ext":false,"idx_exp":false,"idx_exp_url":"","idx_exp_time":"0","file_ext_time":"0","name":"base_santos","description":"sasasasasa","password":"sasasasasa","color":""},"content":[{"field":{"name":"campo","alias":"campo","description":"efewfewfewfew","datatype":"Text","required":false,"multivalued":false,"indices":["Textual"]}},{"group":{"metadata":{"name":"g1","alias":"g1","description":"efewf","multivalued":true},"content":[{"field":{"name":"campo2","alias":"g1_c1","description":"efewvwevew","datatype":"Text","required":false,"multivalued":false,"indices":["Textual"]}},{"group":{"metadata":{"name":"g2","alias":"g2","description":"efewfew","multivalued":true},"content":[{"field":{"name":"campo3","alias":"campo3","description":"efewfewv","datatype":"Text","required":false,"multivalued":false,"indices":["Textual"]}}]}}]}}]}'''


baseteste = json2base(JSON)
BaseTeste = baseteste.metaclass()
G1 = baseteste.metaclass('g1')
G2 = baseteste.metaclass('g2')

class BaseMaluca(BaseTeste):

    def __init__(self, **args):
        super(BaseMaluca, self).__init__(**args)

    @property
    def campo(self):
        return BaseTeste.campo.__get__(self)

    @campo.setter
    def campo(self, v):
        BaseTeste.campo.__set__(self, v)

    @property
    def g1(self):
        return BaseTeste.g1.__get__(self)

    @g1.setter
    def g1(self, v):
        BaseTeste.g1.__set__(self, v)

    def teste_maluco(self, obj_maluco):
        g1_list = [ ]

        for elm in obj_maluco:
            g1 = G1()
            g2_list = []

            for elm2 in elm['g2']:
                g2 = G2()
                g2.campo3 = elm2['campo3']
                g2_list.append(g2)

            g1.campo2=elm['campo2']
            g1.g2 = g2_list
            g1_list.append(g1)

        self.g1 = g1_list
        #BaseTeste.g1.__set__(self, g1_list)

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

    def teste_maluco(self):

        doc = BaseMaluca()
        doc.campo = '1'

        g1 = [{
            'campo2': 'xxxx',
            'g2':[{
                'campo3': 'zzzz'
            },{
                'campo3': 'yyyy'
            }]
        },{
            'campo2': 'aaaa',
            'g2':[{
                'campo3': 'bbbb'
            },{
                'campo3': 'cccc'
            }]
        }]

        doc.teste_maluco(g1)
        j = document2json(baseteste, doc, indent=4)

        assert doc.campo == '1'
        assert doc.g1[0].g2[0].campo3 == 'zzzz'
        assert doc.g1[1].g2[1].campo3 == 'cccc'
        raise Exception(j)





