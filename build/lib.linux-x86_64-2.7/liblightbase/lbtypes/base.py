# -*- coding: utf-8 -*-
from ..lbutils import Property, isiterable

class lbtype(object):
    """ Base for all lbtype classes
        lbtype classes are special classes that
        mimics strong typing in python
    """
    # A type or list of types that this lbtype should allow
    inner_type = None
    
    # Inner value, should not be externally used
    _value = None
    
    # Name of the object
    name = ''
    
    @property
    def inner_types(self):
        """ As inner_type can be a single value or 
            a list of values, inner_types always return
            a list of values
        """
        return self.inner_type if isiterable(self.inner_type, allow_string=False) else (self.inner_type,)
    
    def __eq__(self,value):
        """ Comparing equals with this class
        """
        return self.value == value
    
    def __gt__(self,value):
        """ Comparing greater then with this class
        """
        return self.value > value

    def __ge__(self,value):
        """ Comparing greater or equals with this class
        """
        return self.__eq__(value) or self.__gt__(value)
        
    def __lt__(self,value):
        """ Comparing less then with this class
        """
        return not self.__ge__(value)
    
    def __le__(self,value):
        """ Comparing less or equals with this class
        """
        return not self.__gt__(value)
    
    def __init__(self, value=None, name=''):
        """ Initialize object name and value
        """
        self.name = name
        self.value = value
    
    def __is_valid__(self, value):
        """ Return if the value is an instance of 
            any inner_types. None values are always
            acceptable.
        """
        if value is None:
            return True

        for atype in self.inner_types:
            if isinstance(value,atype):
                return True
        return False
    
    def __call__(self, *args):
        """ When object is called without arguments, return value
            If there is an argument, set value
        """
        if not args:
            return self.value
        self.value = args[0]
        
    def __repr__(self):
        """ Returns visual representation of this object as it is
            in the inner value
        """
        return getattr(self.value,'__repr__',lambda: str(self))()
        
    def __str__(self):
        """ Returns string representation of this object as it is
            in the inner value
        """
        return getattr(self.value,'__str__',lambda: str(self))()
       
    def __xml__(self, doc):
        """ Work with the xml parser, so it can returns the correct
            xml structure for the value
        """
        element = doc.createElement(self.__class__.__name__)
        if self.name:
            element.setAttribute('name',self.name)
        
        if self.value is not None:
            element.appendChild(doc.createTextNode(self.__str__()))
        
        return element
    
    def __parse_string__(self, string):
        """ Translate a string to a valid inner_value
            Try to see if inner_type already knows how
            to do that
        """
        
        for itype in self.inner_types:
            try:
                self.value = itype(string)
                return self.value
            except ValueError:
                pass        
        raise ValueError
        
    def __read_xml__(self,childNodes):
        """ Work with the xml parser, so it can correctly reads
            xml structure of the value
        """
        for childNode in childNodes:
            if childNode.nodeName != '#text':
                continue
            value = childNode.nodeValue.encode('utf-8').strip()
            if not value:
                continue
            return self.__parse_string__(value)
            
    @Property
    def value():
        """ Special property that returns inner value and receive, if valid,
            external values.
        """
        def fget(self):
            return self._value
        
        def fset(self, value):
            if self.__is_valid__(value):
                self._value = value
            else:
                raise ValueError, '%s is not of type %s' %(value, self.inner_type)

        def fdel(self):
            del self._value 
        
        return locals()