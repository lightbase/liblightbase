#
from .base import *
from .standard import *
from .extended import *

def is_lbtype(type_obj, object_only = False):
    """ Verify if type_obj is an instance of lbtype
        If object_only is false, return also true if the class
        descend from lbtype
    """
    if not object_only and isinstance(type_obj, type):
        type_obj = type_obj()
    return isinstance(type_obj, lbtype)

def get_lbtype(type_name, allow_meta=False):
    """ Receive a string and return a lbtype class
        If allow meta is true, it also return a metaclass
        function generator
    """
    if isinstance(type_name, str):
        lbtype_class = globals()[type_name]
    else:
        lbtype_class = type_name
    
    if is_lbtype(lbtype_class):
        return lbtype_class
    
    if not allow_meta:
        raise TypeError('%s is not a valid lbtype' %lbtype_class)
    
    lbtype_function = lbtype_class
    lbtype_class = globals().get('Meta%s' %type_name,None)

    if not is_lbtype(lbtype_class):
        raise TypeError('%s is not a valid lbtype or lbtype meta' %lbtype_function)
    
    return lbtype_function

def pytype2lbtype(type_name, return_class=False):
    """
    Convert a Python type in an LBType
    :param type_name: Python type to be converted
    :return: LBType class name
    """
    get_class = lambda x: globals()[x]
    for lbtype in globals():
        lbtype_class = get_class(lbtype)
        inner_type = getattr(lbtype_class, 'inner_type', None)
        if inner_type == type_name:
            if return_class:
                return getattr(lbtype_class, 'lb_type')
            else:
                class_instance = getattr(lbtype_class, 'lb_type')
                return getattr(class_instance, '__name__')