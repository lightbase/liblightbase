
# -*- coding: utf-8 -*-
import inspect
import json

class BaseDataType():

    """ Base Methods for any Field
    """
    def __init__(self, base, field, id):
        self.base = base
        self.field = field
        self.id = id

    def __call__(self, value):
        if value == '' or value == None:
            if self.field.required:
                raise Exception('ValidationError(%s): Required value not provided.' % self.field.name)
            if value == None:
                self._obj = value
                return value
        try:
            value = self.validate(value)
        except Exception as e:
            raise Exception('ValidationError(%s): %s' % (self.field.name, e))

        if self.field.is_rel:
            path = inspect.currentframe().f_back.f_locals['path']
            path_indices = self._path_indices(path)

            if len(path_indices) > 0:

                _rel_data = self.base.__reldata__[self.id].get(self.field.name)

                if _rel_data is not None:
                    data = self._put_data(_rel_data, path_indices, self.__obj__)
                    self.base.__reldata__[self.id][self.field.name] = data
                else:
                    data = self._put_data(Matrix(), path_indices, self.__obj__)
                    self.base.__reldata__[self.id][self.field.name] = data
            else:
                self.base.__reldata__[self.id][self.field.name] = self.__obj__

        return value

    def _put_data(self, matrix, indices, obj):
        _matrix = matrix
        for i, index in enumerate(indices):
            if i == len(indices) - 1:
                _matrix[index] = obj
            else:
                _matrix = _matrix[index]
        return matrix

    def _path_indices(self, path):
        return [i for i in path if isinstance(i, int)]

    def _encoded(self):
        return '%s' % self.__class__.__name__

    @property
    def __obj__(self):
        return self._obj

    @__obj__.setter
    def __obj__(self, obj):
        if isinstance(self.__pytype__, tuple):
            if not isinstance(obj, self.__pytype__):
                raise Exception('Expected %s but %s found' %
                    (self.get_expected_types(), type(obj).__name__))
        elif not isinstance(obj, self.__pytype__):
            raise Exception('Expected type %s but %s found' %
                (self.__pytype__.__name__, type(obj).__name__))
        self._obj = obj

    def get_expected_types(self):
        expected_types = ''
        for i, pytype in enumerate(self.__pytype__):
            if i > 0: expected_types = ' or ' + expected_types
            expected_types = pytype.__name__ + expected_types 
        return expected_types
                

class Matrix(list):

    def __setitem__(self, index, value):
        try:
            super(Matrix, self).__setitem__(index, value)
        except IndexError:
            for _ in range(index-len(self)+1):
                self.append(None)
            super(Matrix, self).__setitem__(index, value)

    def __getitem__(self, index):
        try:
            return super(Matrix, self).__getitem__(index)
        except IndexError:
            m = Matrix()
            self.__setitem__(index, m)
            return super(Matrix, self).__getitem__(index)

class BaseEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, BaseDataType):
            return obj._encoded()
        else:
            return obj

