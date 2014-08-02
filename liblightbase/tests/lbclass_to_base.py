#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
import sys
from datetime import datetime
from . import load_test_data
#from liblightbase.lbutils import utils
from liblightbase.lbbase.struct import Base
from liblightbase import pytypes
from liblightbase import lbutils
from liblightbase.lbutils import conv
from liblightbase.lbtypes import standard
from liblightbase.lbbase.lbstruct.field import Field
from ..lbutils.const import PYSTR

class TestClassToBase(unittest.TestCase):
    """
    Test convert Python class to LBBase
    """

    def setUp(self):
        self.school = load_test_data.School(
            name='Escola',
            city='Brasília',
            country='BR',
            teachers=[
                {
                    'name': 'Professor 1',
                    'title': 'Doutor'
                },
                {
                    'name': 'Professor 2',
                    'title': 'Mestre'
                }
            ],
            courses=['Computação', 'Matemática'],
            foundation_date=datetime.strptime('2014-08-02', '%Y-%m-%d'),
            address='Rua Saturnino de Brito'
        )
        pass

    def test_class_load(self):
        """
        Test class loaded
        """
        self.assertIsInstance(self.school, load_test_data.School)


    def test_class_types(self):
        """
        Test class types identification
        """
        saida = lbutils.get_attr(self.school)
        print(saida)
        self.assertIsInstance(saida, list)

    def test_pytypes(self):
        """
        Test Pytypes identification
        """
        elm = {
            'name': 'nome',
            'type': PYSTR,
            'value': 'Joãzinho'
        }
        tipo = pytypes.pytype2lbtype(elm['type'])
        print(tipo)
        self.assertEqual(tipo, getattr(standard.Text, '__name__'))

    def test_lbfield(self):
        """
        Test pytype conversion to LB Field
        """
        saida = lbutils.get_attr(self.school)
        lba = conv.attribute2lbfield(saida[0])
        print(lba)
        self.assertIsInstance(lba, Field)

    def test_generate_base(self):
        """
        Test auto generate LB Base from Python object
        """
        lbbase = conv.pyobject2base(self.school)
        fd = open('/tmp/school_base.json', 'w+')
        fd.write(lbbase.json)
        fd.close()
        self.assertIsInstance(lbbase, Base)

    def test_base_conversion(self):
        """
        Test auto generated base json
        """
        lbbase = conv.pyobject2base(self.school)
        j = lbbase.json
        b = conv.json2base(j)

        self.assertIsInstance(b, Base)

    def tearDown(self):
        pass