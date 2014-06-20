
import json
import re
from liblightbase.lbcodecs import *

class reify(object):
    """ Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor."""

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val

def Coerce(type):
    """Coerce a value to a type.
    If the type constructor throws a ValueError, the value will be marked as
    Invalid.
    """
    def f(v):
        try:
            return type(v)
        except ValueError:
            raise ValueError('Expected %s for value: %s' % (type.__name__, v))
    return f


class Object():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def deserialize(string):
    return json2object(string, object_hook=lambda d: Object(**d))

def serialize(obj):
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__
    return object2json(obj, cls=MyEncoder)

def validate_url(url):
    #http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    _url = None
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    try: _url = regex.match(url)
    except: pass
    if _url:
        return _url.string
    else:
        raise ValueError('"%s" is not a valid url' % url)

def typed_getter(prop):
    def __getter__(self):
        return getattr(self, '_' + prop)
    return __getter__

def typed_setter(prop, types):
    def __setter__(self, val):
        if type(val) in types:
            setattr(self, '_' + prop, val)
        else:
            raise TypeError('Expected one type of {} for {}, but got {}'
                .format(str(types), prop, str(type(val))))
    return __setter__

class TypedMetaClass(type):

    def __new__(cls, name, bases, attrs):

        for prop, types in attrs.items():
            if prop.startswith('__'): continue
            attrs[prop] = property(typed_getter(prop), typed_setter(prop, types))

        return super(TypedMetaClass, cls).__new__(cls, name, bases, attrs)



