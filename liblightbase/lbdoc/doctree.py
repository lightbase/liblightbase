
import re
import copy
import jsonpath_rw
from datetime import datetime
from liblightbase import lbutils
from liblightbase.lbdoc.treetypes import Object
from liblightbase.lbdoc.treetypes import Array

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
        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) == 1:
            return matches[0].value
        elif len(matches) > 1:
            return {str(match.full_path): match.value for match in matches}
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))

    def insert_on_leaf(self, branch, path, value):
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
            branch = branch[node]
        try:
            branch[node].append(value)
        except AttributeError:
            raise AttributeError('Structure %s must be array. Use PUT instead.'
                % node)

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
        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) > 0:
            for match in matches:
                lbpath = self.jpath2lbpath(str(match.full_path))
                self.insert_on_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))
        return 0, self.root

    def update_leaf(self, branch, path, value):
        parent = None
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                sname = parent if isinstance(node, int) else node
                value = self.str2lbtype(node,
                    self.base.get_struct(sname),
                    value, 'put')
                break
            branch = branch[node]
            parent = node
        branch[node] = value

    def put_path(self, path, value, fn=None):
        """ 
        This method traverse the tree object following the path, until
        it ends, than update the value to @value.
        @ param path: List of nodes that indicates where to put the value.
        @ param value: The value to update. If the current struct is a group
        then the value may be a JSON value.
        @ returns tree structure.
        """
        # Special treatment for metadata
        if path == ['_metadata', 'dt_idx']:
            self.root[path[0]][path[1]] = datetime\
                .strptime(value, '%d/%m/%Y %H:%M:%S')
            return self.root

        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) > 0:
            for match in matches:
                if fn is not None and not fn(match.value):
                        continue
                lbpath = self.jpath2lbpath(str(match.full_path))
                self.update_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))

        return self.root

    def delete_leaf(self, branch, path):
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                break
            branch = branch[node]
        del branch[node]

    def delete_path(self, path):
        """ 
        This method traverse the tree object following the path, until
        it ends, than deletes the current node.
        @ param path: List of nodes that indicates where to put the value.
        @ returns tree structure.
        """
        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)

        def keyfunc(match):
            # sort by last index descending
            return int(str(match.full_path)[-2:-1])

        if len(matches) > 0:

            if str(matches[0].full_path).endswith(']'):
                # if it is a multivalued field have to sort because need
                # to delete last indexes before firsts
                matches = sorted(matches, key=keyfunc, reverse=True)

            for match in matches:
                lbpath = self.jpath2lbpath(str(match.full_path))
                self.delete_leaf(self.root, lbpath)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))
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

    def lbpath2jpath(self, lbpath):
        dot_notation = '.'.join(lbpath)
        jpath_notation = re.sub(r'(^|\.)([0-9]+|\*)($|\.)',
            r'[\2]\3', dot_notation)
        return jsonpath_rw.parse(jpath_notation)

    def jpath2lbpath(self, jpath):
        lbpath = jpath.replace('.[', '/')\
            .replace('].', '/')\
            .replace('.', '/')
        if lbpath.endswith(']'):
            #remove last char
            lbpath = lbpath[:-1]
        return lbpath.split('/')
