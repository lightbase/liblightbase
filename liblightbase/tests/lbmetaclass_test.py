import unittest
from datetime import datetime
from .. import lbmetaclass
from .. import lbtypes

class lbmetaclass_test(unittest.TestCase):
    def test_metaclass_generation(self):
        test_class = lbmetaclass.generate_class('test_class',[
            { 'name':'name',
              'type':'String',
            },
            { 'name':'age',
              'type':'Integer',
            },
            { 'name':'height',
              'type':'Float',
            }
        ])
        
        obj = test_class()
        obj.name('Fulano de Tal')
        obj['age'] = 23
        obj.height.value = 45.7
        self.assertEqual(obj['name'],'Fulano de Tal')
        self.assertEqual(obj.age.value,23)
        self.assertEqual(obj.height(),45.7)
    
    def test_metaclass_array(self):
        test_class = lbmetaclass.generate_class('test_class',[
            { 'name':'numbers',
              'type':lbtypes.Array('Integer'),
            },
            { 'name':'texts',
              'type':lbtypes.Array('String'),
            },
        ])
        
        obj = test_class()
        obj.texts.append('Value01')
        obj.texts.append(lbtypes.String('Value02'))
        obj.numbers.append(1)
        obj.numbers.append(2)
        self.assertEqual(obj.texts[0],'Value01')
        self.assertEqual(obj.texts[1],'Value02')
        self.assertEqual([text() for text in obj['texts']],['Value01','Value02'])
        self.assertEqual(obj.numbers[0],1)
        self.assertEqual(obj.numbers[1],2)
        self.assertEqual([number() for number in obj['numbers']],[1,2])
        self.assertRaises(ValueError,obj.texts.append,1)
        self.assertRaises(ValueError,obj.numbers.append,'text')
    
    def test_metaclass_custom_type(self):
        class mycustomtype(lbtypes.lbtype):
            inner_type = dict
        test_class = lbmetaclass.generate_class('test_class',[{ 'name':'dic','type':mycustomtype}])
        obj = test_class()
        self.assertRaises(ValueError,obj.dic,'mystring')
        obj['dic'] = { 1:1 }
        self.assertEquals(obj['dic'],{ 1:1 })
        
