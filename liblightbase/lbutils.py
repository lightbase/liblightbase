
import uuid
from copy import deepcopy
import json
import re

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

class FileMask():

    def __init__(self, id_doc, nome_doc, mimetype, uuid):
        self._id_doc = id_doc
        self.nome_doc = nome_doc
        self.mimetype = mimetype
        self.uuid = uuid

    @property
    def _id_doc(self):
        return self.id_doc

    @_id_doc.setter
    def _id_doc(self, id):
        try:
            if id: self.id_doc = int(id)
        except:
            raise Exception('ValueError: id_doc must be integer.')

def is_uuid(id):
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False

class Object():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def deserialize(string):
    if isinstance(string, str):
        string = string.encode('utf-8')
    try:
        return json.loads(string.decode('utf-8'), object_hook=lambda d: Object(**d))
    except Exception as e:
        raise Exception('Could not parse JSON data. Details: %s' % str(e.args[0]))

def serialize(obj):
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__
    return json.dumps(obj, cls=MyEncoder, ensure_ascii=False)

def parse_json(obj):
    if obj is None:
        raise Exception('No JSON data supplied.')
    if type(obj) is dict:
        return obj
    if isinstance(obj, str):
        obj = obj.encode('utf-8')
    try:
        obj = json.loads(obj.decode('utf-8'))
        return obj
    except Exception as e:
        raise Exception('Could not parse JSON data. Details: %s' % str(e.args[0]))

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
