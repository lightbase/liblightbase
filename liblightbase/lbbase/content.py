# -*- coding: utf-8 -*-
from liblightbase.lbbase.lbstruct.field import Field
from liblightbase.lbbase.lbstruct.group import Group
from liblightbase import lbutils

class Content(list):
    """
    Class to hold contents in Groups and bases
    """

    def __init__(self):
        #FIXME: Fix repeated name check for structs in global scope

        # @property __structs__:
        self.__structs__ = { }

        # @property asdict:
        self.asdict = [ ]

        # Initialize super class constructor
        super(Content, self).__init__()

    @property
    def json(self):
        return lbutils.object2json(self)

    def __getitem__(self, index):
        return super(Content, self).__getitem__(index)

    def __setitem__(self, index, struct):
        if isinstance(struct, Field):
            structname = struct.name
        elif isinstance(struct, Group):
            structname = struct.metadata.name
        else:
            raise ValueError('This should be an instance of Field or Group.\
                Instead it is %s' % struct)
        if structname in self.__structs__:
            raise ValueError('Duplicated struct name: %s' % structname)

        self.asdict.append(struct.asdict)
        self.__structs__[structname] = struct
        return super(Content, self).__setitem__(index, struct)

    def append(self, struct):
        if isinstance(struct, Field):
            structname = struct.name
        elif isinstance(struct, Group):
            structname = struct.metadata.name
        else:
            raise ValueError('This should be an instance of Field or Group.\
                Instead it is %s' % struct)

        if structname in self.__structs__:
            raise ValueError('Duplicated struct name: %s' % structname)

        self.asdict.append(struct.asdict)
        self.__structs__[structname] = struct
        return super(Content, self).append(struct)

    def _encoded(self):
        """

        :return: Object JSON
        """

        return self.asdict