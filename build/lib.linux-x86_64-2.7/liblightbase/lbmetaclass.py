# -*- coding: utf-8 -*-
import lbtypes

class LBMetaClass(object):
    """ This the metaclass, where all lightbase 
        classes will be generated from
    """
    _structure = []
    def __init__(self, *kwargs):
        """ Create lbtypes instances of all values in _structure
        """
        for attr in self._structure:    
            typeclass = lbtypes.get_lbtype(attr['type'])      
            setattr(self, attr['name'], typeclass(name=attr['name'], value=attr.get('value',None)))
    
    def __setattr__(self, attr, value):
        """ When setting an attribute, if it is a lbtype,
            set the lbtype value instead
        """
        method = getattr(self,attr,None)
        if method and lbtypes.is_lbtype(method):
            self[attr] = value
        else:
            object.__setattr__(self, attr, value)
    
    def __get_lbtype_attr__(self, attr):
        """ Returns the attribute if the attribute
            is an lbtype
        """
        attr = getattr(self,attr)
        if not lbtypes.is_lbtype(attr):
            raise KeyError,'%s is not a valid lbtype attribute' %attr
        return attr	
      
    def __getitem__(self, attr):
        """ When working as a dict, this class return the lbtype value
        """
        return self.__get_lbtype_attr__(attr).value
    
    def __setitem__(self, attr, value):
        """ When working as a dict, this class sets the lbtype value
        """
        self.__get_lbtype_attr__(attr).value = value
    
    def __delitem__(self, attr):
        """ When working as a dict, this class del the lbtype attribute
        """
        attr = self.__get_lbtype_attr__(attr)
        del attr    

def generate_class(name, structure):
    """ Generate a child class from LBMetaClass
    """
    class new_class(LBMetaClass): pass
    new_class.__name__ = name
    new_class._structure = structure
    return new_class
