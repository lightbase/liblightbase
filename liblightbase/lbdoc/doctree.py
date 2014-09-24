
import copy
from datetime import datetime
from liblightbase import lbutils
from liblightbase.lbdoc.treetypes import Object

class DocumentTree():

    def __init__(self, root, base=None, create_path=False):
        self.base = base
        self.create_path = create_path
        self.root= Object(root,
            base=self.base,
            create_path=self.create_path)

    def prune(self, root=None, nodes=[]):
        """ 
        @param root: Tree structure to prune 
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
        """ 
        This method traverse the tree object following the path, until
        it finds tyhe value, than return it.
        @ param path: List of nodes that indicates where to get the value.
        @ returns value contained in Tree indicated by path.
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
        """ 
        This method traverse the tree object following the path, until
        it ends, than appends @value to the current node, that must be
        an array.
        @ param path: List of nodes that indicates where to set the value.
        @ param value: The value to set. If the current struct is a group,
        then the value may be a JSON value.
        @ returns tree structure.
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
        """ 
        This method traverse the tree object following the path, until
        it ends, than update the value to @value.
        @ param path: List of nodes that indicates where to put the value.
        @ param value: The value to update. If the current struct is a group
        then the value may be a JSON value.
        @ returns tree structure.
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
        """ 
        This method traverse the tree object following the path, until
        it ends, than deletes the current node.
        @ param path: List of nodes that indicates where to put the value.
        @ returns tree structure.
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
