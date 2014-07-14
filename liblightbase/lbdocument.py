
from liblightbase import lbutils
from datetime import datetime
import copy

class DocumentMetadata(object):

    """ 
    The document metadata is all data related to the document. The main purpose
    of metadata is to facilitate in the discovery of relevant information, more 
    often classified as resource discovery.
    """

    def __init__(self, id_doc, dt_doc, dt_last_up, dt_idx=None,
            dt_del=None):

        """ Class constructor. Sets document metadata attributes. 
        """

        # @property id_doc: The primary key for document's table 
        # and uniquely identify each document in the table.
        self.id_doc = id_doc

        # @property dt_doc: The document's creation date 
        # (date and time).
        self.dt_doc = dt_doc

        # @property dt_last_up: The document's last updating date 
        # (date and time).
        self.dt_last_up = dt_last_up

        # @property dt_idx: The document's date (date and time) of indexing. 
        # All routines that index the document must fill this field.
        self.dt_idx = dt_idx

        # @property dt_del: The document's date (date and time) of deletion. 
        # This date is filled when he normal deletion process failed when 
        # deleting the document index. When it happens, the document is cleared 
        # up, leaving only it's metadata.
        self.dt_del = dt_del

    @property
    def __dict__(self):
        """ Dictionary format of document metadata model.
        """
        return {
           'id_doc' : self.id_doc,
           'dt_doc' : self.dt_doc,
           'dt_last_up' : self.dt_last_up,
           'dt_idx' : self.dt_idx,
           'dt_del' : self.dt_del
        }

    def _attr_setter(self, attr, value, accepted_types):
        """
        Class custom setter. Verify if value is instance of one of 
        accepted_types and set private attribute to class.
        @param attr: attribute name.
        @param value: attribute value to be setted.
        @param accepted_types: tuple of types.
        """
        try:
            assert(isinstance(value, accepted_types))
        except AssertionError:
            raise TypeError('{0} must be of type {1}'.format(
                attr, accepted_types))
        else:
            setattr(self, '_' + attr, value)

    @property
    def id_doc(self):
        """ @property id_doc getter
        """
        return self._id_doc

    @id_doc.setter
    def id_doc(self, value):
        """ @property id_doc setter
        """
        accepted_types = (int,)
        self._attr_setter('id_doc', value, accepted_types)

    @property
    def dt_doc(self):
        """ @property dt_doc getter
        """
        return self._dt_doc

    @dt_doc.setter
    def dt_doc(self, value):
        """ @property dt_doc setter
        """
        accepted_types = (datetime,)
        self._attr_setter('dt_doc', value, accepted_types)

    @property
    def dt_last_up(self):
        """ @property dt_last_up getter
        """
        return self._dt_last_up

    @dt_last_up.setter
    def dt_last_up(self, value):
        """ @property dt_last_up setter
        """
        accepted_types = (datetime,)
        self._attr_setter('dt_last_up', value, accepted_types)

    @property
    def dt_idx(self):
        """ @property dt_idx getter
        """
        return self._dt_idx

    @dt_idx.setter
    def dt_idx(self, value):
        """ @property dt_idx setter
        """
        accepted_types = (datetime, type(None))
        self._attr_setter('dt_idx', value, accepted_types)

    @property
    def dt_del(self):
        """ @property dt_del getter
        """
        return self._dt_del

    @dt_del.setter
    def dt_del(self, value):
        """ @property dt_del setter
        """
        accepted_types = (datetime, type(None))
        self._attr_setter('dt_del', value, accepted_types)

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
