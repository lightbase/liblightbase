
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

        # @property __structs__: Dictionary in the format {structure name:
        # structure}. This data structure helps to get structure by it's name,
        # instead of navigating the list.
        self.__structs__ = { }

        # @property asdict: Dictonary (actually list) format of content model. 
        self.asdict = [ ]

        # Initialize super class constructor
        super(Content, self).__init__()

    @property
    def json(self):
        # @property json: JSON format of group model. 
        return lbutils.object2json(self.asdict)

    def __getitem__(self, index):
        """ x.__getitem__(y) <==> x[y]
        """
        return super(Content, self).__getitem__(index)

    def __setitem__(self, index, struct):
        """ x.__setitem__(y, z) <==> x[y] = z
        """
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
        """ L.append(object) -- append object to end
        """
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
