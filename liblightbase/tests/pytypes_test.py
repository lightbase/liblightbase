import unittest
from datetime import datetime
from liblightbase import pytypes

class pytypes_test(unittest.TestCase):

    def setUp(self):
        pass

    def test_string_init_value(self):
        self.assertEqual(pytypes.String('test').value ,'test')
        self.assertEqual(pytypes.String('test_unicode').value ,'test_unicode')
        self.assertEqual(pytypes.String(None).value ,None)
        self.assertEqual(pytypes.String().value ,None)
        
        self.assertRaises(ValueError,pytypes.String,1)
        self.assertRaises(ValueError,pytypes.String,1.1)
        self.assertRaises(ValueError,pytypes.String,11111111111111111111)
        
    def test_string_set_and_get(self):
        test_string = pytypes.String()
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
        self.assertEqual(pytypes.Integer(1).value,1)
        self.assertEqual(pytypes.Integer(11111111).value,11111111)
        self.assertEqual(pytypes.Integer(None).value ,None)
        self.assertEqual(pytypes.Integer().value ,None)
        
        self.assertRaises(ValueError,pytypes.Integer,1.1)
        self.assertRaises(ValueError,pytypes.Integer,'test')
        self.assertRaises(ValueError,pytypes.Integer,'test')
        
    def test_integer_set_and_get(self):
        test_integer = pytypes.Integer()
        test_integer.value = 1
        self.assertEqual(test_integer.value,1)
        test_integer.value = 1111111
        self.assertEqual(test_integer.value,1111111)
        
        with self.assertRaises(ValueError) as cm:
            test_integer.value = 'test'
        
        with self.assertRaises(ValueError) as cm:
            test_integer.value = 'test'
            
        with self.assertRaises(ValueError) as cm:
            test_integer.value = 1.1

    def test_float_init_value(self):
        self.assertEqual(pytypes.Float(1.1).value, 1.1)
        self.assertEqual(pytypes.Float(None).value ,None)
        self.assertEqual(pytypes.Float().value ,None)
        
        self.assertRaises(ValueError,pytypes.Float,1)
        self.assertRaises(ValueError,pytypes.Float,11111111111111111111)
        self.assertRaises(ValueError,pytypes.Float,'test')
        self.assertRaises(ValueError,pytypes.Float,'test')
        
    def test_float_set_and_get(self):
        test_float = pytypes.Float()
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
        self.assertEqual(pytypes.DateTime(my_date).value, my_date)
        self.assertEqual(pytypes.Float(None).value ,None)
        self.assertEqual(pytypes.Float().value ,None)

    def test_datetime_set_and_get(self):
        my_date = datetime.now()
        test_datetime = pytypes.DateTime()
        test_datetime.value = my_date
        self.assertEqual(test_datetime.value,my_date)
    
    def test_multiple(self):
        mul = pytypes.Multiple({ 'text': 'String', 'number': 'Integer'})
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
        dt = pytypes.DateTime()
        dt(my_date)
        self.assertEqual(dt(), my_date)
        st = pytypes.String()
        st('test')       
        self.assertEqual(st(), 'test')
        it = pytypes.Integer()
        it(11)       
        self.assertEqual(it(), 11)
        fl = pytypes.Float()
        fl(1.1)       
        self.assertEqual(fl(), 1.1)

    def test_long_init_value(self):
        self.assertEqual(pytypes.Long(11111111111111111111).value,11111111111111111111)
        self.assertEqual(pytypes.Long(None).value ,None)
        self.assertEqual(pytypes.Long().value ,None)

        self.assertRaises(ValueError,pytypes.Long,1)
        self.assertRaises(ValueError,pytypes.Long,1.1)
        self.assertRaises(ValueError,pytypes.Long,'test')
        self.assertRaises(ValueError,pytypes.Long,'test')

    def test_long_set_and_get(self):
        test_long = pytypes.Long()
        test_long.value = 11111111111111111111
        self.assertEqual(test_long.value,11111111111111111111)

        with self.assertRaises(ValueError) as cm:
            test_long.value = 'test'

        with self.assertRaises(ValueError) as cm:
            test_long.value = 'test'

        with self.assertRaises(ValueError) as cm:
            test_long.value = 1.1

        with self.assertRaises(ValueError) as cm:
            test_long.value = 1


    def tearDown(self):
        pass