# -*- coding: utf-8 -*-
import sys
from .base import lbtype
from datetime import datetime
from dateutil.parser import parse as date_parser

    
class String(lbtype):
    """ lbtype string class
    """
    inner_type = str

class Integer(lbtype):
    """ lbtype integer class
    """
    inner_type = int

class Float(lbtype):
    """ lbtype float class
    """
    inner_type = float

class DateTime(lbtype):
    """ lbtype datetime class
    """
    inner_type = datetime
    def __parse_string__(self, string):
        self.value = date_parser(string)
        return self.value
        
class Long(lbtype):
    """ lbtype integer class
    Hacked to work on Python 2 and Python 3
    """
    if sys.version > '3':
        inner_type = int
    else:
        inner_type = long