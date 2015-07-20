
class Array(list):

    def __init__(self, obj, base, create_path=False):
        self.base = base
        self.create_path = create_path
        super(Array, self).__init__(obj)

    def tolist(self):
        def conv(v):
            if isinstance(v, Object):
                return v.todict()
            elif isinstance(v, Array):
                return v.tolist()
            else:
                return v
        return [conv(v) for v in self]

    def __getitem__(self, index):
        return super(Array, self).__getitem__(index)
        """
        try:
            return super(Array, self).__getitem__(index)
        except IndexError:
            if self.create_path:
                reg_obj = Object({}, self.base, create_path=self.create_path)
                self.__setitem__(index, reg_obj)
                return super(Array, self).__getitem__(index)
            else:
                raise IndexError('Array index out of range.')
        """

    def __setitem__(self, index, item):
        super(Array, self).__setitem__(index, item)
        """
        try:
            super(Array, self).__setitem__(index, item)
        except IndexError:
            for _ in range(index-len(self)+1):
                reg_obj = Object({}, self.base, create_path=self.create_path)
                self.append(reg_obj)
            super(Array, self).__setitem__(index, item)
        """

class Object(dict):

    def __init__(self, obj, base, create_path=False):
        self.base = base
        self.create_path = create_path
        super(Object, self).__init__(obj)

    def todict(self):
        """ Convert self to dict object
        """
        def conv(v):
            if isinstance(v, Object):
                return v.todict()
            elif isinstance(v, Array):
                return v.tolist()
            else:
                return v
        out = dict()
        for k, v in self.items():
            out[k] = conv(v)
        return out

    def _getregobj(self, sname):
        """ @param sname: structure name to find
            @ returns Array or Object

            This method gets the base structure (Field/Group), and returns
            a empty instance depending on structure's multivalue attribute.
        """
        struct = self.base.get_struct(sname)
        if struct.is_group:
            if struct.metadata.multivalued:
                 return Array([], self.base, create_path=self.create_path)
            else:
                return Object({}, self.base, create_path=self.create_path)
        else:
            if struct.multivalued:
                return Array([], self.base, create_path=self.create_path)
        return Object({}, self.base, create_path=self.create_path)

    def __getitem__(self, key):
        try:
            item = super(Object, self).__getitem__(key)
            if isinstance(item, dict):
                item = Object(item, self.base, create_path=self.create_path)
                self.__setitem__(key, item)
            elif isinstance(item, list):
                item = Array(item, self.base, create_path=self.create_path)
                self.__setitem__(key, item)
        except KeyError:
            if self.create_path:
                self.__setitem__(key, self._getregobj(key))
                return super(Object, self).__getitem__(key)
            else:
                raise KeyError('Field %s does not exist' % key)
        else:
            return item

    def __setitem__(self, key, item):
        super(Object, self).__setitem__(key, item)
