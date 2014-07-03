import unittest
from datetime import datetime
from .. import lbmetaclass
from .. import lbtypes
from .. import lbxml

class lbxml_test(unittest.TestCase):
    def setUp(self):
        self.test_class = lbmetaclass.generate_class('test_class',[
            { 'name':'text',
              'type':'String',
            },
            { 'name':'number',
              'type':'Integer',
            },
            { 'name':'listnumber',
              'type':lbtypes.Array('Integer'),
            },
            { 'name':'listmultiple',
              'type':lbtypes.Array(lbtypes.Multiple({
                'text_inner':'String',
                'number_inner':'Integer'
              })),
            },
            
        ])
        
        self.test_class_xml = '<?xml version="1.0" ?><class name="test_class"><String name="text"/><Integer name="number"/><Array name="listnumber" type="Integer"/><Array name="listmultiple" type="Multiple"><Multiple><String name="text_inner"/><Integer name="number_inner"/></Multiple></Array></class>'
        self.test_obj = self.test_class()
        self.test_obj.text = 'Texto'
        self.test_obj.number = 123
        self.test_obj.listnumber.append(234)
        self.test_obj.listnumber.append(456)
        self.test_obj.listmultiple.append({ 'text_inner':'Texto Interno', 'number_inner':789 } )
        self.test_obj.listmultiple.append({ 'text_inner':'Texto Interno 2', 'number_inner':890 } )
        self.test_obj_xml = '<?xml version="1.0" ?><object name="test_class"><String name="text">Texto</String><Integer name="number">123</Integer><Array name="listnumber" type="Integer"><Integer>234</Integer><Integer>456</Integer></Array><Array name="listmultiple" type="Multiple"><Multiple><String name="text_inner">Texto Interno</String><Integer name="number_inner">789</Integer></Multiple><Multiple><String name="text_inner">Texto Interno 2</String><Integer name="number_inner">890</Integer></Multiple></Array></object>'
        
    def test_class_to_xml(self):
        result = lbxml.class_to_xml(self.test_class, pretty=False)
        self.assertEqual(result, self.test_class_xml)
        
    def test_object_to_xml(self):
        result = lbxml.object_to_xml(self.test_obj, pretty=False)
        self.assertEqual(result, self.test_obj_xml)
        
    def test_xml_to_class(self):
        cls = lbxml.xml_to_class(self.test_class_xml)
        obj = cls()
        self.assertTrue(hasattr(obj,'text'))
        self.assertTrue(hasattr(obj,'number'))
        self.assertTrue(hasattr(obj,'listnumber'))
        self.assertTrue(hasattr(obj,'listmultiple'))
        self.assertFalse(obj['text'])
        self.assertFalse(obj['number'])
        self.assertFalse(obj['listnumber'])
        self.assertFalse(obj['listmultiple'])
        
    def test_xml_to_object(self):
        obj = lbxml.xml_to_object(self.test_obj_xml)
        self.assertTrue(hasattr(obj,'text'))
        self.assertTrue(hasattr(obj,'number'))
        self.assertTrue(hasattr(obj,'listnumber'))
        self.assertTrue(hasattr(obj,'listmultiple'))
        self.assertEqual(obj['text'], 'Texto')
        self.assertEqual(obj['number'], 123)
        self.assertEqual(obj['listnumber'][0].value, 234)
        self.assertEqual(obj['listnumber'][1].value, 456)
        self.assertEqual(obj['listmultiple'][0]['text_inner'],'Texto Interno')
        self.assertEqual(obj['listmultiple'][1]['number_inner'],890)
        
