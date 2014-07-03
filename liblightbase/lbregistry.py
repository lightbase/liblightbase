from liblightbase.lbutils import deserialize
from liblightbase.lbutils import serialize
from liblightbase.lbcodecs import json2object as parse_json
from liblightbase.lbutils import TypedMetaClass
from datetime import datetime


NONETYPE = type(None)

class RegistryMetadata(metaclass=TypedMetaClass):

    id_reg = (int,)
    dt_reg = (datetime,)
    dt_last_up = (datetime,)
    dt_index_tex = (datetime, NONETYPE)
    dt_reg_del = (datetime, NONETYPE)

    def __init__(self, id_reg, dt_reg, dt_last_up, dt_index_tex=None, dt_reg_del=None):
        self.id_reg = id_reg
        self.dt_reg = dt_reg
        self.dt_last_up = dt_last_up
        self.dt_index_tex = dt_index_tex
        self.dt_reg_del = dt_reg_del

    @property
    def __dict__(self):
        return {
            'id_reg' : self.id_reg,
            'dt_reg' : self.dt_reg,
            'dt_last_up' : self.dt_last_up,
            'dt_index_tex' : self.dt_index_tex,
            'dt_reg_del' : self.dt_reg_del
        }

class Registry():

    def __init__(self, base, registry):
        self.base = base
        self.registry = deserialize(registry)

    def find_base_object(self, path):
        split = path.split('.')
        base = self.base
        for name in split:
            name = name.split('[')[0]
            base = self.get_structure(base, name)
        return base

    def get_structure(self, base, name):
        for content in base.content:
            if content.name == name:
                return content
        raise Exception('Key "%s" is not present in base definitions.' % name)

    def get_path(self, path, return_obj=False):
        try:
            expr = 'self.registry.' + path
            value = eval(expr)
            if return_obj:
                if hasattr(value, '__dict__'): return value.__dict__
                else: return value
            else: return serialize(value)

        except AttributeError as e:
            raise AttributeError('Could not get path. Details: %s' % str(e.args[0]))

        except TypeError as e:
            raise TypeError('Registry attribute is not multivalued.')

        except SyntaxError as e:
            raise SyntaxError('Not a valid path.')

        except IndexError as e:
            raise IndexError('List index out of range.')

    def set_path(self, path, value):
        try: current_value = self.get_path(path, return_obj=True)
        except (IndexError, AttributeError): current_value = None
        base = self.find_base_object(path)
        if not base.multivalued.multivalued:
            raise Exception('This method is only allowed for multivalued Fields/Groups')
        if hasattr(base, 'datatype') and hasattr(base, 'indices'): #if isinstance(base, Field):
            # It's a field, no need for parsing value
            pass
        else:
            # It's a group, need for parsing value
            try: value = parse_json(value)
            except: raise Exception('Expected dictionary for Group value.')
        if not current_value:
            index = 0
            value = [value]
        elif type(current_value) is list:
            index = len(current_value)
            current_value.append(value)
            value = current_value
        else:
            raise Exception('Expected list for current registry value, but type is %s' % type(current_value))
        expr = 'self.registry.' + path + ' = value'
        try: exec(expr)
        except Exception as e:
            raise Exception('Could not set path. Details: %s' % str(e.args[0]))

        _return = {
            'DEFAULT': str(index),
            'json_reg': serialize(self.registry),
            'json_path': None,
            'new_path': path + '[' + str(index) + ']',
            'new_value': None
        }

        #return index, serialize(self.registry)
        return _return

    def put_path(self, path, value):
        # Does path exist ?
        current_value = self.get_path(path, return_obj=True)
        put_index = path[-1:] == ']'
        # Alright, lets do the job.
        base = self.find_base_object(path)
        if hasattr(base, 'datatype') and hasattr(base, 'indices'):
            if base.multivalued and not put_index:
                # It's a multivalued field, need to parse value
                try: value = parse_json(value)
                except: raise Exception('Expected list for multivalued Field.')
        else:
            # It's a group, need to parse value
            try: value = parse_json(value)
            except: raise Exception('Expected list of dictionaries for Group.')
        expr = 'self.registry.' + path + ' = value'
        try: exec(expr)
        except Exception as e:
            raise Exception('Could not update path. Details: %s' % str(e.args[0]))

        _return = {
            'DEFAULT': 'UPDATED',
            'json_reg': serialize(self.registry),
            'new_value': None,
        }

        return _return

    def delete_path(self, path):
        base = self.find_base_object(path)
        # Does path exist ?
        self.get_path(path, return_obj=True)
        # Alright, lets do the job.
        #put_index = path[-1:] == ']'
        #if base.multivalued.multivalued or not put_index:
        #    raise Exception('This method is only allowed for multivalued Fields/Groups')
        expr = 'del self.registry.' + path
        try: exec(expr)
        except Exception as e:
            raise Exception('Could not delete path. Details: %s' % str(e.args[0]))

        _return = {
            'DEFAULT': 'DELETED',
            'json_reg': serialize(self.registry),
        }

        return _return

