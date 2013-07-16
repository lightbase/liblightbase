# -*- coding: utf-8 -*-
from base import lbtype
from datetime import datetime
from dateutil.parser import parse as date_parser
    
class String(lbtype):
    """ lbtype string class
    """
    inner_type = (str, unicode)

class Integer(lbtype):
    """ lbtype integer class
    """
    inner_type = (int, long)

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
        
