
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

        # @property __snames__: List of structure names. Used for preventing
        # duplicated names.
        self.__snames__ = [ ]

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
            self.__snames__ +=  [structname]

        elif isinstance(struct, Group):
            structname = struct.metadata.name
            self.__snames__ +=  [structname]
            duplicated = self.find_duplicated(self.__snames__,
                                              struct.content.__snames__)
            if duplicated:
                raise NameError('Duplicated names detected: %s' % duplicated)
            else:
                self.__snames__ +=  struct.content.__snames__
                self.__structs__.update(struct.content.__structs__)

        else:
            raise TypeError('This should be an instance of Field or Group.\
                Instead it is %s' % struct)

        self.asdict.append(struct.asdict)
        self.__structs__[structname] = struct
        return super(Content, self).__setitem__(index, struct)

    def append(self, struct):
        """ L.append(object) -- append object to end
        """
        if isinstance(struct, Field):
            structname = struct.name
            self.__snames__ +=  [structname]

        elif isinstance(struct, Group):
            structname = struct.metadata.name
            self.__snames__ +=  [structname]
            duplicated = self.find_duplicated(self.__snames__,
                                              struct.content.__snames__)
            if duplicated:
                raise NameError('Duplicated names detected: %s' % duplicated)
            else:
                self.__snames__ +=  struct.content.__snames__
                self.__structs__.update(struct.content.__structs__)

        else:
            raise TypeError('This should be an instance of Field or Group.\
                Instead it is %s' % struct)

        self.asdict.append(struct.asdict)
        self.__structs__[structname] = struct
        return super(Content, self).append(struct)
