
from liblightbase import lbutils
from datetime import datetime
import copy

NONETYPE = type(None)

class DocumentMetadata(object):
    __metaclass__=lbutils.TypedMetaClass

    id_doc = (int,)
    dt_doc = (datetime,)
    dt_last_up = (datetime,)
    dt_idx = (datetime, NONETYPE)
    dt_del = (datetime, NONETYPE)

    def __init__(self, id_doc, dt_doc, dt_last_up, dt_idx=None,
            dt_del=None):

        self.id_doc = id_doc
        self.dt_doc = dt_doc
        self.dt_last_up = dt_last_up
        self.dt_idx = dt_idx
        self.dt_del = dt_del

    @property
    def __dict__(self):
        return {
           'id_doc' : self.id_doc,
           'dt_doc' : self.dt_doc,
           'dt_last_up' : self.dt_last_up,
           'dt_idx' : self.dt_idx,
           'dt_del' : self.dt_del
        }

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
        return {k: conv(v) for k, v in self.items()}

    def _getregobj(self, sname):
        """ @param sname: structure name to find
            @ returns Array or Object

            This method gets the base structure (Field/Group), and returns
            a empty instance depending on structure's multivalue attribute.
        """
        if self.base.get_struct(sname).multivalued:
            return Array([], self.base, create_path=self.create_path)
        else:
            return Object({}, self.base, create_path=self.create_path)

    def __getitem__(self, key):
        try:
            item = super(Object, self).__getitem__(key)
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

class Tree():

    def __init__(self, root, base=None, create_path=False):
        self.base = base
        self.create_path = create_path
        self.root= Object(root,
                         base=self.base,
                         create_path=self.create_path
                         )

    def prune(self, root=None, nodes=[]):
        """ @param root: Tree structure to prune 
            @param nodes: Nodes to keep after pruning (all other nodes will be 
            removed)
            @return: New tree structure pruned, or None, if no node was pruned.
        """
        if root is None:
            root = self.root

        if isinstance(root, dict):
            retVal = {}
            for key in root:
                if key in nodes:
                    retVal[key] = copy.deepcopy(root[key])
                elif isinstance(root[key], list) or isinstance(root[key], dict):
                    child = self.prune(root[key], nodes)
                    if child:
                        retVal[key] = child
            if retVal:
                 return retVal
            else:
                 return None
        elif isinstance(root, list):
            retVal = []
            for entry in root:
                child = self.prune(entry, nodes)
                if child:
                    retVal.append(child)
            if retVal:
                return retVal
            else:
                return None

    def get_path(self, path):
        """ @ param path: List of nodes that indicates where to get the value.
            @ returns value contained in Tree indicated by path.

            This method traverse the tree object following the path, until
            it finds tyhe value, than return it.
        """

        root = self.root
        for node in path:
            node = self.toint(node)
            try:
                root = root[node]
            except KeyError:
                raise KeyError('Field %s does not exist.' % node)
            except TypeError:
                raise TypeError('array index must be int, not "%s".' % node)
            except IndexError:
                raise IndexError('array index out of range')

        return root

    def set_path(self, path, value):
        """ @ param path: List of nodes that indicates where to set the value.
            @ param value: The value to set. If the current struct is a group,
            then the value may be a JSON value.
            @ returns tree structure.

            This method traverse the tree object following the path, until
            it ends, than appends @value to the current node, that must be
            an array.
        """

        root = self.root
        parent = None
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                sname = parent if isinstance(node, int) else node
                value = self.str2lbtype(node,
                                       self.base.get_struct(sname),
                                       value)
                break
            parent = node
            root = root[node]
        try:
            root[node].append(value)
        except AttributeError:
            raise AttributeError('Structure %s must be array. Use PUT instead.'
                % node)
        return len(root[node])-1, self.root

    def put_path(self, path, value):
        """ @ param path: List of nodes that indicates where to put the value.
            @ param value: The value to update. If the current struct is a group
            then the value may be a JSON value.
            @ returns tree structure.

            This method traverse the tree object following the path, until
            it ends, than update the value to @value.
        """
        root = self.root

        # Special treatment for metadata
        if path == ['_metadata', 'dt_idx']:
            root[path[0]][path[1]] = datetime\
                .strptime(value, '%d/%m/%Y %H:%M:%S')
            return self.root

        parent = None
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                sname = parent if isinstance(node, int) else node
                value = self.str2lbtype(node,
                                       self.base.get_struct(sname),
                                       value, 'put')
                break
            root = root[node]
            parent = node
        root[node] = value
        return self.root

    def delete_path(self, path):
        """ @ param path: List of nodes that indicates where to put the value.
            @ returns tree structure.

            This method traverse the tree object following the path, until
            it ends, than deletes the current node.
        """

        root = self.root
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                break
            root = root[node]
        del root[node]
        return self.root

    def toint(self, obj):
        try: return int(obj)
        except: return obj

    def str2lbtype(self, node, struct, value, method=None):
        if struct.is_group:
            _lbtype = lbutils.json2object(value)
        elif isinstance(node, int):
            _lbtype = struct._datatype.__schema__.cast_str(value)
        elif struct.multivalued and method == 'put':
            _lbtype = lbutils.json2object(value)
        elif value == 'null':
            _lbtype = None
        else:
            _lbtype = struct._datatype.__schema__.cast_str(value)
        return _lbtype
