
import re
import copy
import jsonpath_rw
from datetime import datetime
from liblightbase import lbutils
from liblightbase.lbdoc.treetypes import Object
from liblightbase.lbdoc.treetypes import Array

# delete path - DocumentTree() __init__(self, root, base=None, create_path=False)
class DocumentTree():

    def __init__(self, root, base=None, create_path=False):
        self.base = base
        self.create_path = create_path

        # delete path - self.root
        self.root = Object(root,
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
            saida = dict()
            for match in matches:
                saida[str(match.full_path)] = match.value

            return saida

            #return {str(match.full_path): match.value for match in matches}
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

    def set_path(self, path, fn):
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
                ok, value = fn(match)
                if not ok:
                    continue
                lbpath = self.jpath2lbpath(str(match.full_path))
                self.insert_on_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))
        return self.root

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

    def put_path(self, path, fn):
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
            actual_value = self.root['_metadata']['dt_idx']
            match = type("Match", (), {'value': actual_value})()
            ok, value = fn(match)
            if value == 'null': value = None
            self.root['_metadata']['dt_idx'] = value
            return self.root

        # Special treatment for the root path "/"
        if path == ['', '']:
            path = ['$']

        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) > 0:
            for match in matches:
                ok, value = fn(match)
                if not ok:
                    continue
                lbpath = self.jpath2lbpath(str(match.full_path))
                if lbpath == ['$']:
                    self.root = Object(value,
                                       base=self.base,
                                       create_path=self.create_path)
                else:
                    self.update_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))

        return self.root

    def patch_leaf(self, branch, path, value):
        """
        Traverses the object tree through path then partially updates
        it with 'value'. Only fields present in 'value' will be changed.
        Everything else in path remains the same.
        """
        parent = None
        node = ''
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                sname = parent if isinstance(node, int) else node
                value = self.str2lbtype(node,
                    self.base.get_struct(sname),
                    value, 'patch')
                break
            branch = branch[node]
            parent = node

        self.patch_leaf_rec(branch, node, value)

        return self.root

    def patch_leaf_rec(self, branch, node, new_value):
        """
        Recursily updates a branch and its leafs with values in 'new_value'
        """
        if node == '':
            if isinstance(new_value, dict):
                for key, value in new_value.items():
                    self.patch_leaf_rec(branch, key, new_value[key])
            else:
                # TODO: ERROR -> root must always be dict
                pass
        elif isinstance(branch, dict) and node not in branch:
            branch[node] = new_value
        else:
            if isinstance(new_value, dict):
                for key, value in new_value.items():
                    self.patch_leaf_rec(branch[node], key, new_value[key])
            elif isinstance(new_value, list):
                for idx, item in enumerate(new_value):
                    if len(branch[node]) > idx:
                        self.patch_leaf_rec(branch[node], idx, item)
                    else:
                        branch[node].append(item)
            else:
                branch[node] = new_value

    def patch_path(self, path, fn):
        """
        This method traverse the tree object following the path, until
        it ends, then patches the value to @value.
        @ param path: List of nodes that indicates where to put the value.
        @ param value: The value to update. If the current struct is a group
        then the value may be a JSON value.
        @ returns tree structure.
        """
        # Special treatment for metadata
        if path == ['_metadata', 'dt_idx']:
            actual_value = self.root['_metadata']['dt_idx']
            match = type("Match", (), {'value': actual_value})()
            ok, value = fn(match)
            if value == 'null': value = None
            self.root['_metadata']['dt_idx'] = value
            return self.root

        # Special treatment for the root path "/"
        if path == ['', '']:
            path = ['$']

        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) > 0:
            for match in matches:
                ok, value = fn(match)
                if not ok:
                    continue
                lbpath = self.jpath2lbpath(str(match.full_path))
                if lbpath == ['$']:
                    lbpath = []
                self.patch_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))

        return self.root

    def merge_leaf(self, branch, path, value):
        """
        Traverses the object tree through path then partially updates
        it with 'value'. Only fields present in 'value' will be changed.
        Everything else in path remains the same.
        """
        parent = None
        node = ''
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                sname = parent if isinstance(node, int) else node
                value = self.str2lbtype(node,
                    self.base.get_struct(sname),
                    value, 'patch')
                break
            branch = branch[node]
            parent = node

        self.merge_leaf_rec(branch, node, value)

        return self.root

    def merge_leaf_rec(self, branch, node, new_value):
        """
        Recursily updates a branch and its leafs with values in 'new_value'
        Manual mode
        """
        if node == '':
            if isinstance(new_value, dict):
                for key, value in new_value.items():
                    self.merge_leaf_rec(branch, key, new_value[key])
            else:
                # TODO: ERROR -> root must always be dict
                pass
        elif node not in branch:
            branch[node] = new_value
        else:
            if isinstance(new_value, dict):
                for key, value in new_value.items():
                    self.merge_leaf_rec(branch[node], key, new_value[key])
            elif isinstance(new_value, list):
                for idx, item in enumerate(new_value):
                    if item not in branch[node]:
                        branch[node].append(item)
            else:
                branch[node] = new_value

    def merge_path(self, path, fn):
        """
        This method traverse the tree object following the path, until
        it ends, then patches the value to @value.
        @ param path: List of nodes that indicates where to put the value.
        @ param value: The value to update. If the current struct is a group
        then the value may be a JSON value.
        @ returns tree structure.
        """
        # Special treatment for metadata
        if path == ['_metadata', 'dt_idx']:
            actual_value = self.root['_metadata']['dt_idx']
            match = type("Match", (), {'value': actual_value})()
            ok, value = fn(match)
            if value == 'null': value = None
            self.root['_metadata']['dt_idx'] = value
            return self.root

        # Special treatment for the root path "/"
        if path == ['', '']:
            path = ['$']

        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) > 0:
            for match in matches:
                ok, value = fn(match)
                if not ok:
                    continue
                lbpath = self.jpath2lbpath(str(match.full_path))
                if lbpath == ['$']:
                    lbpath = []
                self.merge_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))

        return self.root

    def manual_leaf(self, branch, path, value):
        """
        Traverses the object tree through path then partially updates
        it with 'value'. Only fields present in 'value' will be changed.
        Everything else in path remains the same.
        """
        parent = None
        node = ''
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                sname = parent if isinstance(node, int) else node
                value = self.str2lbtype(node,
                    self.base.get_struct(sname),
                    value, 'patch')
                break
            branch = branch[node]
            parent = node

        self.manual_leaf_rec(branch, node, value)

        return self.root

    def manual_leaf_rec(self, branch, node, new_value):
        """
        Recursily updates a branch and its leafs with values in 'new_value'
        Manual mode
        """
        if node == '':
            if isinstance(new_value, dict):
                for key, value in new_value.items():
                    self.manual_leaf_rec(branch, key, new_value[key])
            else:
                # TODO: ERROR -> root must always be dict
                pass
        elif isinstance(branch, dict) and node not in branch:
            branch[node] = new_value
        else:
            if isinstance(new_value, dict):
                for key, value in new_value.items():
                    self.manual_leaf_rec(branch[node], key, new_value[key])
            elif isinstance(new_value, list) and self.is_list_descriptor(new_value):
                self.manual_list(branch[node], new_value)
            elif isinstance(new_value, list):
                for idx, item in enumerate(new_value):
                    if len(branch[node]) > idx:
                        self.manual_leaf_rec(branch[node], idx, item)
                    else:
                        branch[node].append(item)
            else:
                branch[node] = new_value

    def manual_path(self, path, fn):
        """
        This method traverse the tree object following the path, until
        it ends, then patches the value to @value.
        @ param path: List of nodes that indicates where to put the value.
        @ param value: The value to update. If the current struct is a group
        then the value may be a JSON value.
        @ returns tree structure.
        """
        # Special treatment for metadata
        if path == ['_metadata', 'dt_idx']:
            actual_value = self.root['_metadata']['dt_idx']
            match = type("Match", (), {'value': actual_value})()
            ok, value = fn(match)
            if value == 'null': value = None
            self.root['_metadata']['dt_idx'] = value
            return self.root

        # Special treatment for the root path "/"
        if path == ['', '']:
            path = ['$']

        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)
        if len(matches) > 0:
            for match in matches:
                ok, value = fn(match)
                if not ok:
                    continue
                lbpath = self.jpath2lbpath(str(match.full_path))
                if lbpath == ['$']:
                    lbpath = []
                self.manual_leaf(self.root, lbpath, value)
        else:
            raise IndexError('Could not find any matches for index -> %s' %
                '/'.join(path))

        return self.root

    def is_list_descriptor(self, the_list):
        """
        Checks if the_list constains 'update list descriptors':
        { "$set#[pos]" : "value" } -> edit value in position [pos]
        { "$add" : "value" } -> add value at the end of list
        { "$add#[pos]" : "value" } -> add value in position [pos] and push back the rest
        { "$remove": null } -> remove last value form list
        { "$remove#[pos]" : null } -> remove value in position [pos] and pull back the rest
        { "$multi#[pos-start]#[pos-end]" : [ "value-pos-start", ..., "value-pos-end" ] -> change all values 
                      from position [pos-start] to position [pos-end] (inclusive)
        """
        first_item = the_list[0] if len(the_list) > 0 else None

        if isinstance(first_item, dict):
            for key in first_item:
                if key.startswith("$"):
                    return True

        return False

    def manual_list(self, doc_list, update_doc_list):
        """
        Updates doc_list using descriptors contained in update_doc_list.
        See is_list_descriptor() for a list of possible descriptors.
        """
        valid_descriptors = {
            "$set": self.manual_list_set,
            "$add": self.manual_list_add,
            "$remove": self.manual_list_remove,
            "$multi": self.manual_list_multi
        }

        for descriptor in update_doc_list:
            for key, value in descriptor.items():
                args = key.split("#")
                command = args[0]
                args = args[1:]

                command_func = valid_descriptors.get(command, None)
                if command_func is None:
                    # TODO: ERROR invalid command
                    raise KeyError(command + ': invalid list decriptor')

                command_func(doc_list, value, *args)

    def manual_list_set(self, doc_list, value, *args):
        # TODO: check args size, check if it's int
        pos = int(args[0])
        if (len(doc_list) > pos):
            if isinstance(value, list) and self.is_list_descriptor(value):
                self.manual_list(doc_list[pos], value)
            else:
                self.manual_leaf_rec(doc_list, pos, value)
        else:
            # TODO: ERROR position doesn't exist
            pass

    def manual_list_add(self, doc_list, value, *args):
        if len(args) > 0:
            # TODO: check if its int
            pos = int(args[0])
            doc_list.insert(pos, value)
        else:
            # append to the end of list
            doc_list.append(value)

    def manual_list_remove(self, doc_list, value, *args):
        if len(args) > 0:
            # TODO: check if its int
            pos = int(args[0])
            del doc_list[pos]
        else:
            # remove last
            doc_list.pop()

    def manual_list_multi(self, doc_list, value, *args):
        if len(args) > 1 and isinstance(value, list):
            pos_start = int(args[0])
            pos_end = int(args[1])
                        
            num_elements = pos_end - pos_start + 1
            if num_elements != len(value):
                # TODO ERROR
                pass

            current_pos = pos_start

            for i in range(0, num_elements):
                if (len(doc_list) > current_pos):
                    if isinstance(value[i], dict):
                        self.update_dict(doc_list[current_pos], value[i])
                    elif isinstance(value[i], list) and self.is_list_descriptor(value[i]):
                        self.update_list(doc_list[current_pos], value[i])
                    else:
                        doc_list[current_pos] = value[i]
                else:
                    # TODO: add to end or fail?
                    # adding to the end
                    doc_list.append(value[i])

                current_pos += 1
        else:
            # TODO: ERROR
            pass

    # delete path - delete_leaf(self, branch, path)
    def delete_leaf(self, branch, path):
        for ipath, node in enumerate(path):
            node = self.toint(node)
            if ipath == len(path) - 1:
                break
            branch = branch[node]
        del branch[node]

    # delete path - delete_path(self, path, fn)
    def delete_path(self, path, fn):
        """ 
        This method traverse the tree object following the path, until
        it ends, than deletes the current node.
        @ param path: List of nodes that indicates where to put the value.
        @ returns tree structure.
        """
        jpath = self.lbpath2jpath(path)
        matches = jpath.find(self.root)

        # TODO: Pq esse troço tah aki? Quem usa?
        def keyfunc(match):
            # sort by last index descending
            return int(str(match.full_path)[-2:-1])

        if len(matches) > 0:

            if str(matches[0].full_path).endswith(']'):
                # if it is a multivalued field have to sort because need
                # to delete last indexes before firsts
                #matches = sorted(matches, key=keyfunc, reverse=True)
                matches.reverse()

            for match in matches:
                ok = fn(match)
                if not ok:
                    continue
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
        elif struct.multivalued and method == 'patch':
            _lbtype = lbutils.json2object(value)
        elif value == 'null':
            _lbtype = None
        else:
            _lbtype = struct._datatype.__schema__.cast_str(value)
        return _lbtype

    # delete path - lbpath2jpath(self, lbpath)
    def lbpath2jpath(self, lbpath):
        dot_notation = '.'.join(lbpath)
        jpath_notation = re.sub(r'(^|\.)([0-9]+|\*)($|\.)',
            r'[\2]\3', dot_notation)
        return jsonpath_rw.parse(jpath_notation)

    # delete path - jpath2lbpath(self, jpath)
    def jpath2lbpath(self, jpath):
        lbpath = jpath.replace('.[', '/')\
            .replace('].', '/')\
            .replace('.', '/')
        if lbpath.endswith(']'):
            #remove last char
            lbpath = lbpath[:-1]
        return lbpath.split('/')
