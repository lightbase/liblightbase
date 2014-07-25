# -*- coding: utf-8 -*-
from liblightbase.lbbase.lbstruct.field import Field
from liblightbase.lbbase.lbstruct.group import Group
from liblightbase import lbutils

class Content(list):
    """
    The content is a list of structures that compose the current schema.
    Structures may also have metadata and content, giving the current schema 
    a recursive modeling.
    """

    def __init__(self):
        # @property __structs__: All structures from this level to down.
        # Dictionary in the format {structure name: structure}. This data
        # structure helps to get structure by it's name,
        # instead of navigating the list.
        self.__allstructs__ = { }

        # @property __structs__: Structures from this level only. Dictionary
        # in the format {structure name: structure}. This data structure helps
        # to get structure by it's name, instead of navigating the list.
        self.__structs__ = { }

        # @property __snames__: List of all structure names. Used for preventing
        # duplicated names.
        self.__allsnames__ = [ ]

        # @property __snames__: List of structure names on this level only.
        self.__snames__ = [ ]

        # @property __snames__: List of structure names (on this level only)
        # that are required fields.
        self.__rnames__ = []

        # @property asdict: Dictonary (actually list) format of content model. 
        self.asdict = [ ]

        # Initialize super class constructor
        super(Content, self).__init__()

    @property
    def json(self):
        """ @property json: JSON format of group model. 
        """
        return lbutils.object2json(self.asdict)

    def __getitem__(self, index):
        """ x.__getitem__(y) <==> x[y]
        """
        return super(Content, self).__getitem__(index)

    def find_duplicated(self, xset, yset):
        zset = xset + yset
        duplicated = set()
        if not len(set(zset)) == len(xset) + len(yset):
            duplicated = set([val for val in zset if zset.count(val) > 1])
        return duplicated

    def __setitem__(self, index, struct):
        """ x.__setitem__(y, z) <==> x[y] = z
        """
        if isinstance(struct, Field):
            structname = struct.name
            self.__allsnames__ +=  [structname]
            self.__snames__ +=  [structname]
            if struct.required:
                self.__rnames__ +=  [structname]

        elif isinstance(struct, Group):
            structname = struct.metadata.name
            self.__allsnames__ +=  [structname]
            self.__snames__ +=  [structname]
            duplicated = self.find_duplicated(self.__allsnames__,
                                              struct.content.__allsnames__)
            if duplicated:
                raise NameError('Duplicated names detected: %s' % duplicated)
            else:
                self.__allsnames__ +=  struct.content.__allsnames__
                self.__allstructs__.update(struct.content.__allstructs__)

        else:
            raise TypeError('This should be an instance of Field or Group.\
                Instead it is %s' % struct)

        self.asdict.append(struct.asdict)
        self.__allstructs__[structname] = struct
        self.__structs__[structname] = struct
        return super(Content, self).__setitem__(index, struct)

    def append(self, struct):
        """ L.append(object) -- append object to end
        """
        if isinstance(struct, Field):
            structname = struct.name
            self.__allsnames__ +=  [structname]
            self.__snames__ +=  [structname]
            if struct.required:
                self.__rnames__ +=  [structname]

        elif isinstance(struct, Group):
            structname = struct.metadata.name
            self.__allsnames__ +=  [structname]
            self.__snames__ +=  [structname]
            duplicated = self.find_duplicated(self.__allsnames__,
                                              struct.content.__allsnames__)
            if duplicated:
                raise NameError('Duplicated names detected: %s' % duplicated)
            else:
                self.__allsnames__ +=  struct.content.__allsnames__
                self.__allstructs__.update(struct.content.__allstructs__)

        else:
            raise TypeError('This should be an instance of Field or Group.\
                Instead it is %s' % struct)

        self.asdict.append(struct.asdict)
        self.__allstructs__[structname] = struct
        self.__structs__[structname] = struct
        return super(Content, self).append(struct)
