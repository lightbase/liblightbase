# -*- coding: utf-8 -*-
from base import lbtype
from ..lbutils import Property
from __init__ import get_lbtype, is_lbtype

class MetaMultiple(lbtype):
    """ It's a dict like lbtype, that allow
        lbtypes values
    """
    _structure = {}
    def __init__(self, value=None, name=''):
        """ Generate from structure, 
            local lbtypes, to be used as object
            parameters.
        """
        for key,atype in self._structure.items():    
            typeclass = get_lbtype(atype)      
            setattr(self, key, typeclass(name=key))
        if value:
            self.value = value
        self.name = name
    
    def __get_lbtype_attr__(self, attr):
        """ Return attribute, if attr string
            is a valid lbtype
        """
        attr = getattr(self,attr)
        if not is_lbtype(attr):
            raise KeyError,'%s is not a valid lbtype attribute' %attr
        return attr 
        
    def __setattr__(self, attr, value):
        """ set inner values as attribute attribution
        """
        method = getattr(self,attr,None)
        if method and is_lbtype(method):
            self[attr] = value
        else:
            object.__setattr__(self, attr, value)
        
    def __getitem__(self, attr):
        """ get inner values as a dict
        """
        return self.__get_lbtype_attr__(attr).value
    
    def __setitem__(self, attr, value):
        """ set inner values as a dict
        """
        self.__get_lbtype_attr__(attr).value = value
    
    def __delitem__(self, attr):
        """ removes inner values as a dict
        """
        attr = self.__get_lbtype_attr__(attr)
        del attr  

    def __xml__(self, doc):
        """ Work with the xml parser, so it can returns the correct
            xml structure of all inner values
        """
        element = doc.createElement(self.__class__.__name__)
        if self.name:
            element.setAttribute('name',self.name)
        for key in self._structure:
            option = getattr(self, key, None)
            if option is not None:
                element.appendChild(option.__xml__(doc))
        return element

    def __read_xml__(self,childNodes):
        """ Work with the xml parser, so it can correctly reads
            xml structure of all inner values
        """        
        for childNode in childNodes:
            if childNode.nodeName == '#text':
                continue
            name = childNode.getAttribute('name')
            getattr(self,name).__read_xml__(childNode.childNodes)
        return self.value        
        
    @Property
    def value():
        """ Convert a dict to this lbtype, and this lbtype to dict
        """
        def fget(self):
            dlist = [(key,self.__get_lbtype_attr__(key).value) for key in self._structure ]
            return dict(dlist)
        
        def fset(self, dic):
            for key,value in dic.items():
                self.__get_lbtype_attr__(key).value = value

        def fdel(self):
            for key in self._structure:
                attr = self.__get_lbtype_attr__(key)
                del attr
        
        return locals()
        
def Multiple(structure):
    """ Returns, based on structure, a MetaMultiple
        child class
    """
    class Multiple(MetaMultiple): pass
    
    # structure can be list for xml parsing compatibility
    if isinstance(structure, list):
        structure = dict([(attr['name'],attr['type'])  for attr in structure])
    
    for key in structure:
        structure[key] = get_lbtype(structure[key])
    Multiple._structure = structure
    return Multiple 
    
class MetaArray(list, lbtype):
    """ It's a list like lbtype class
    """
    def __init__(self, *args, **kwargs):
        """ This init mixes list __init__
            with lbtype __init__
        """
        if kwargs.has_key('name'):
            self.name = kwargs['name']
            del kwargs['name']
        
        if kwargs.has_key('value'):
            if kwargs['value']:
                self.value = kwargs['value']
            del kwargs['value']
        
        list.__init__(self, *args, **kwargs)
        
    def __get_inner_value__(self, value):
        """ Support function that returns
            value always as inner_type
        """
        if not self.__is_valid__(value):
            value = self.inner_type(value)
        return value()

    def __setitem__(self, key, value):
        """ Replaces list __setitem__ verifying if
            value is valid
        """
        value = self.__get_inner_value__(value)
        list.__setitem__(self, key, value)
            
    def append(self, value):
        """ Replaces list append verifying if
            value is valid
        """
        value = self.__get_inner_value__(value)
        list.append(self,value)
    
    def extend(self,iterable):
        """ Replaces list extend verifying if
            value is valid
        """
        for value in self.iterable:
            self.append(value)
    
    def insert(self, index, object):
        """ Replaces list insert verifying if
            value is valid
        """
        value = self.__get_inner_value__(object)
        list.insert(self,index,object)
    
    def __xml__(self, doc):
        """ Work with the xml parser, so it can returns the correct
            xml structure for the value
        """
        element = doc.createElement(self.__class__.__name__)
        if self.name:
            element.setAttribute('name',self.name)
        element.setAttribute('type',self.inner_type.__name__)
        values = self.value
        
        if not values:
            inner_obj = self.inner_type()
            
            if inner_obj.value is not None:
                element.appendChild(inner_obj.__xml__(doc))
            
        for value in values:
            element.appendChild(value.__xml__(doc))
        return element

    def __read_xml__(self,childNodes):
        """ Work with the xml parser, so it can correctly reads
            xml structure of the value
        """
        self.value = []
        for childNode in childNodes:
            if childNode.nodeName == '#text':
                continue
            value = self.inner_type().__read_xml__(childNode.childNodes)
            self.append(value)
        return self.value
        
    @Property
    def value():
        """ Returns and converts any list to
            lbtype Array
        """
        def fget(self):
            return [self.inner_type(value) for value in self ]
        
        def fset(self, value_list):
            while self: 
                self.__delitem__(0)
            
            for value in value_list:
                self.append(self.__get_inner_value__(value))
        
        return locals()

def Array(inner_type):
    """ Returns, based on inner_type, a MetaArray
        child class
    """
    class Array(MetaArray): pass
    
    # structure can be list for xml parsing compatibility
    if isinstance(inner_type, list):
        inner_type = inner_type[0]['type']
        
    Array.inner_type = get_lbtype(inner_type)
    return Array
