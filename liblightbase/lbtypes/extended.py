
from liblightbase import lbutils
from liblightbase.lbtypes import BaseDataType
from liblightbase.lbutils.const import PYSTR
from uuid import UUID, uuid3


class FileMask(object):

    """ Represents a Generic File Mask
    """

    def __init__(self, id_file, filename, mimetype, filesize, uuid):
        if id_file is not None:
            self.id_file = UUID(id_file)
        else:
            self.id_file = id_file
        self.filename = filename
        self.mimetype = mimetype
        self.filesize = filesize
        if uuid is not None:
            self.uuid = UUID(uuid)
        else:
            self.uuid = uuid

    @property
    def __dict__(self):
        return dict(
            id_file= self.id_file,
            filename = self.filename,
            mimetype = self.mimetype,
            filesize = self.filesize,
            uuid = self.uuid,
        )

    @property
    def id_file(self):
        """ @property id_file getter
        """
        if self._id_file:
            return str(self._id_file)
        return self._id_file

    @id_file.setter
    def id_file(self, value):
        """ @property id_file setter
        """
        accepted_types = (UUID, type(None))
        if isinstance(value, accepted_types):
            self._id_file = value
        else:
            raise TypeError('id_file must be of type %s but got %s.' % (
                accepted_types, value))

    @property
    def filename(self):
        """ @property filename getter
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        """ @property filename setter
        """
        accepted_types = (PYSTR, type(None))
        if isinstance(value, accepted_types):
            self._filename= value
        else:
            raise TypeError('filename must be of type %s but got %s.' % (
                accepted_types, value))

    @property
    def mimetype(self):
        """ @property mimetype  getter
        """
        return self._mimetype

    @mimetype.setter
    def mimetype(self, value):
        """ @property mimetype  setter
        """
        accepted_types = (PYSTR, type(None))
        if isinstance(value, accepted_types):
            self._mimetype = value
        else:
            raise TypeError('mimetype must be of type %s but got %s.' % (
                accepted_types, value))

    @property
    def filesize(self):
        """ @property filesize  getter
        """
        return self._filesize

    @filesize.setter
    def filesize (self, value):
        """ @property filesize  setter
        """
        accepted_types = (int, type(None))
        if isinstance(value, accepted_types):
            self._filesize = value
        else:
            raise TypeError('filesize must be of type %s but got %s.' % (
                accepted_types, value))

    @property
    def uuid(self):
        """ @property uuid getter
        """
        if self._uuid:
            return str(self._uuid)
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        """ @property uuid setter
        """
        accepted_types = (UUID, type(None))
        if isinstance(value, accepted_types):
            self._uuid = value
        else:
            msg = 'Invalid UUID: {}'
            raise TypeError(msg.format(str(value)))

class FileExtension(BaseDataType):

    """ Represents an extension for file-based Fields
    """
    def __init__(self, base, field, id):
        super(FileExtension, self).__init__(base, field, id)

    @staticmethod
    def cast_str(value):
        return lbutils.json2object(value)

    def __call__(self, value):
        if value is None:
            return value
        try:
            filemask = FileMask(**value)
        except TypeError as e:
            msg = 'Structure {}: Malformed file mask. {}'
            raise Exception(msg.format(self.field.name,
                e))

        filemask = filemask.__dict__
        if any([filemask[v] for v in filemask]):

            id_file = filemask.pop('id_file')
            try:
                namespace = UUID(filemask['uuid'])
            except TypeError:
                raise TypeError('%s is not a valid uuid' % filemask['uuid'])

            name = str(hash(frozenset(filemask.items())))

            try:
                assert id_file == str(uuid3(namespace, name))
            except AssertionError:
                raise ValueError('Mask modified. id_file do not match file mask')

            filemask['id_file'] = id_file
            self.base.__files__[self.id].append(id_file)
            return filemask
        else:
            return filemask
