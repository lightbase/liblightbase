# -*- coding: utf-8 -*-
import sys
from .base import lbtype
from datetime import datetime
from dateutil.parser import parse as date_parser
from ..lbtypes.standard import *
from ..lbutils.const import PYSTR, PYUNICODE
    
class String(lbtype):
    """ lbtype string class
    """
    inner_type = str
    lb_type = Text

class BaseString(lbtype):
    """ lbtype string class
    """
    inner_type = PYSTR
    lb_type = Text

class Unicode(lbtype):
    """ lbtype string class
    """
    inner_type = PYUNICODE
    lb_type = Text

class Integer(lbtype):
    """ lbtype integer class
    """
    inner_type = int
    lb_type = Integer

class Float(lbtype):
    """ lbtype float class
    """
    inner_type = float
    lb_type = Decimal

class DateTime(lbtype):
    """ lbtype datetime class
    """
    inner_type = datetime.datetime
    lb_type = DateTime
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

    lb_type = Integer