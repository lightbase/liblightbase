import unittest
from datetime import datetime
from .. import lbtypes

class lbtypes_test(unittest.TestCase):
    def test_string_init_value(self):
        self.assertEqual(lbtypes.String('test').value ,'test')
        self.assertEqual(lbtypes.String('test_unicode').value ,'test_unicode')
        self.assertEqual(lbtypes.String(None).value ,None)
        self.assertEqual(lbtypes.String().value ,None)
        
        self.assertRaises(ValueError,lbtypes.String,1)
        self.assertRaises(ValueError,lbtypes.String,1.1)
        self.assertRaises(ValueError,lbtypes.String,11111111111111111111)
        
    def test_string_set_and_get(self):
        test_string = lbtypes.String()
        test_string.value = 'test'
        self.assertEqual(test_string.value ,'test')
        test_string.value = 'test_unicode'
        self.assertEqual(test_string.value ,'test_unicode')
        
        with self.assertRaises(ValueError) as cm:
            test_string.value = 1
        with self.assertRaises(ValueError) as cm:
            test_string.value = 1.1
        with self.assertRaises(ValueError) as cm:
            test_string.value = 11111111111111111111

    def test_integer_init_value(self):
        self.assertEqual(lbtypes.Integer(1).value,1)
        self.assertEqual(lbtypes.Integer(11111111111111111111).value,11111111111111111111)
        self.assertEqual(lbtypes.Integer(None).value ,None)
        self.assertEqual(lbtypes.Integer().value ,None)
        
        self.assertRaises(ValueError,lbtypes.Integer,1.1)
        self.assertRaises(ValueError,lbtypes.Integer,'test')
        self.assertRaises(ValueError,lbtypes.Integer,'test')
        
    def test_integer_set_and_get(self):
        test_integer = lbtypes.Integer()
        test_integer.value = 1
        self.assertEqual(test_integer.value,1)
        test_integer.value = 11111111111111111111
        self.assertEqual(test_integer.value,11111111111111111111)
        
        with self.assertRaises(ValueError) as cm:
            test_integer.value = 'test'
        
        with self.assertRaises(ValueError) as cm:
            test_integer.value = 'test'
            
        with self.assertRaises(ValueError) as cm:
            test_integer.value = 1.1

    def test_float_init_value(self):
        self.assertEqual(lbtypes.Float(1.1).value, 1.1)
        self.assertEqual(lbtypes.Float(None).value ,None)
        self.assertEqual(lbtypes.Float().value ,None)
        
        self.assertRaises(ValueError,lbtypes.Float,1)
        self.assertRaises(ValueError,lbtypes.Float,11111111111111111111)
        self.assertRaises(ValueError,lbtypes.Float,'test')
        self.assertRaises(ValueError,lbtypes.Float,'test')
        
    def test_float_set_and_get(self):
        test_float = lbtypes.Float()
        test_float.value = 1.1
        self.assertEqual(test_float.value,1.1)

        with self.assertRaises(ValueError) as cm:
            test_float.value = 1
                    
        with self.assertRaises(ValueError) as cm:
            test_float.value = 11111111111111111111
            
        with self.assertRaises(ValueError) as cm:
            test_float.value = 'test'
        
        with self.assertRaises(ValueError) as cm:
            test_float.value = 'test'
            
    def test_float_init_value(self):
        self.assertEqual(lbtypes.Float(1.1).value, 1.1)
        self.assertEqual(lbtypes.Float(None).value ,None)
        self.assertEqual(lbtypes.Float().value ,None)
        
        self.assertRaises(ValueError,lbtypes.Float,1)
        self.assertRaises(ValueError,lbtypes.Float,11111111111111111111)
        self.assertRaises(ValueError,lbtypes.Float,'test')
        self.assertRaises(ValueError,lbtypes.Float,'test')
        
    def test_float_set_and_get(self):
        test_float = lbtypes.Float()
        test_float.value = 1.1
        self.assertEqual(test_float.value,1.1)

        with self.assertRaises(ValueError) as cm:
            test_float.value = 1
                    
        with self.assertRaises(ValueError) as cm:
            test_float.value = 11111111111111111111
            
        with self.assertRaises(ValueError) as cm:
            test_float.value = 'test'
        
        with self.assertRaises(ValueError) as cm:
            test_float.value = 'test'

    def test_datetime_init_value(self):
        my_date = datetime.now()
        self.assertEqual(lbtypes.DateTime(my_date).value, my_date)
        self.assertEqual(lbtypes.Float(None).value ,None)
        self.assertEqual(lbtypes.Float().value ,None)

    def test_datetime_set_and_get(self):
        my_date = datetime.now()
        test_datetime = lbtypes.DateTime()
        test_datetime.value = my_date
        self.assertEqual(test_datetime.value,my_date)
    
    def test_multiple(self):
        mul = lbtypes.Multiple({ 'text': 'String', 'number': 'Integer'})
        obj = mul()
        obj['text'] = 'my text'
        obj['number'] = 11
        self.assertEqual(obj.text.value ,'my text')
        self.assertEqual(obj.number.value , 11)
        self.assertEqual(obj.value , { 'text': 'my text', 'number': 11 })
        obj.value = { 'text': 'text 2', 'number': 22 }
        self.assertEqual(obj.text.value ,'text 2')
        self.assertEqual(obj.number.value , 22)
        self.assertEqual(obj.value , { 'text': 'text 2', 'number': 22 })
        with self.assertRaises(AttributeError) as cm:
            obj.value = { 'otherstuff': 'error' }
    
    def test_class_call_method(self):
        my_date = datetime.now()
        dt = lbtypes.DateTime()
        dt(my_date)
        self.assertEqual(dt(), my_date)
        st = lbtypes.String()
        st('test')       
        self.assertEqual(st(), 'test')
        it = lbtypes.Integer()
        it(11)       
        self.assertEqual(it(), 11)
        fl = lbtypes.Float()
        fl(1.1)       
        self.assertEqual(fl(), 1.1)
        
    def setUp(self):
        pass

