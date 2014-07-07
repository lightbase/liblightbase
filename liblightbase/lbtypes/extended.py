
from liblightbase import lbutils
from liblightbase.lbtypes import BaseDataType
import glob
import os
import base64
import datetime
import uuid
import tempfile

class FileMask(object):
    """ Represents a Generic File Mask
    """
    __metaclass__=lbutils.TypedMetaClass

    id_file = (int,)
    filename = (str, type(None))
    mimetype = (str, type(None))
    filesize = (int, type(None))
    uuid = (str, type(None))

    def __init__(self, id_file, filename, mimetype, filesize, uuid=None):
        self.id_file = id_file
        self.filename = filename
        self.mimetype = mimetype
        self.filesize = filesize
        self.uuid = uuid

    @property
    def __dict__(self):
        return dict(
            id_file= self.id_file,
            filename = self.filename,
            mimetype = self.mimetype,
            filesize = self.filesize
        )

class FileExtension(BaseDataType):

    """ Represents an extension for file-based Fields
    """
    def __init__(self, base, field, id, tmp_dir=None):
        super(FileExtension, self).__init__(base, field, id)
        #import lbgenerator
        #self.tmp_dir = lbgenerator.config.TMP_DIR + '/lightbase_tmp_storage/' +\
        #    self.base.metadata.name
        #self.entity = lbgenerator.model.file_entity(self.base.metadata.name)
        self.tmp_dir = tmp_dir
        if dir is not None:
            self.tmp_dir = tempfile.gettempdir() + '/lightbase_tmp_storage/' + self.base.metadata.name
        else:
            self.tmp_dir = tmp_dir + '/lightbase_tmp_storage/' + self.base.metadata.name
        self.entity = FileEntity(self.base, self.field)

        self.asdict = {
            'id_file': "Integer",
            'filename': "Text",
            'mimetype': "Text",
            'filesize': "Integer"
        }


    def _encoded(self):
        """

        :return: Object JSON
        """

        return self.asdict

    @staticmethod
    def cast_str(value):
        return lbutils.json2object(value)

    def __call__(self, value):
        """ @param value: string or dictionary. If string, must be an uuid 
            object (new file). If dictionary, must be a file mask (new or
            existent file)

            This method should return a dictonary in the form described by 
            self._encoded().
        """
        mask = None

        if value is None:
            return None

        if isinstance(value, str):
            if self.is_uuid(value):
                # New coming file.
                mask = self.build_file_mask(value)
            else:
                raise TypeError('Malformed mask: unrecognized pattern %s' % value)

        elif isinstance(value, dict):
            mask = self.get_file_mask(value)

            if self.is_uuid(mask.uuid):
                # New coming file.
                mask = self.build_file_mask(mask.uuid)
            else:
                # Existent file. 
                self.base.__files__[self.id].append(mask.id_file)

        else:
            raise TypeError('Malformed mask: Expected dict or str, but found %s' % type(value).__name__)

        assert(isinstance(mask, FileMask))

        return mask.__dict__

    def get_file_mask(self, value):
        try:
            return FileMask(**value)
        except TypeError as e:
            raise Exception('Malformed mask: %s' % e)

    def build_file_mask(self, value):
        tmp_file = self.find_tmp_file(value)
        mask = self.save_file(tmp_file)
        return mask

    def find_tmp_file(self, _uuid):
        tmp_file = None
        for file_path in glob.glob(self.tmp_dir + '/' + _uuid + '*'):
            tmp_file = open(file_path, 'rb')
        if tmp_file is None:
            raise Exception('Could not find temporary file %s on disk' % _uuid)
        return tmp_file

    def get_size(self, fileobject):
        fileobject.seek(0, 2) # move the cursor to the end of the file
        size = fileobject.tell()
        fileobject.seek(0) # move the cursor to the begin of the file
        return size

    def save_file(self, tmp_file):
        fake_name = os.path.split(tmp_file.name)[1]
        split = fake_name.split('.')

        uuid = split.pop(0)
        file_name_encoded = split.pop()
        filename = base64.urlsafe_b64decode(file_name_encoded.encode('utf-8')).decode('utf-8')
        mimetype = '.'.join(split).replace('-', '/', 1)
        filesize = self.get_size(tmp_file)
        id_file = self.entity.next_id()

        dt_ext_text = None
        field_indices = [index.index for index in self.field.indices]
        if 'Nenhum' in field_indices:
            dt_ext_text = datetime.datetime.now()

        self.base.__cfiles__[self.id].append({
           'id_file': id_file,
           'id_doc': self.id,
           'file': tmp_file.read(),
           'filename': filename,
           'filesize': filesize,
           'mimetype': mimetype,
           'filetext': None,
           'dt_ext_text': dt_ext_text
        })

        tmp_file.close()
        os.remove(tmp_file.name)

        return FileMask(id_file, filename, mimetype, filesize)

    def is_uuid(self, id):
        if id is None:
            return False
        try:
            uuid.UUID(id)
            return True
        except ValueError:
            return False


class FileEntity(object):
    """
    Class to get file information from Lightbase
    """
    def __init__(self, base, field):
        self.base = base
        self.field = field

    def next_id(self):
        """
        Method to return next available ID on Lightbase Database

        FIXME: Implment rest operation

        :return: Next available ID
        """
        return 1