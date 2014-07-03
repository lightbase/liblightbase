
from liblightbase.lbutils import reify
from liblightbase.lbutils import TypedMetaClass
from liblightbase.lbtypes import BaseDataType
import lbgenerator
import glob
import os
import base64
import datetime
import uuid

class FileMask(metaclass=TypedMetaClass):
    """ Represents a Generic File Mask
    """

    id_doc = (int,)
    nome_doc = (str, type(None))
    mimetype = (str, type(None))
    size = (int, type(None))
    uuid = (str, type(None))

    def __init__(self, id_doc, nome_doc, mimetype, size, uuid=None, **kw):
        self.id_doc = id_doc
        self.nome_doc = nome_doc
        self.mimetype = mimetype
        self.size = size
        self.uuid = uuid

    @property
    def __dict__(self):
        return dict(
            id_doc = self.id_doc,
            nome_doc = self.nome_doc,
            mimetype = self.mimetype,
            size = self.size
        )

class FileExtension(BaseDataType):

    """ Represents an extension for file-based Fields
    """
    def __init__(self, base, field, id):
        super(FileExtension, self).__init__(base, field, id)
        self.tmp_dir = lbgenerator.config.TMP_DIR + '/lightbase_tmp_storage/' + self.base.name
        self.entity = lbgenerator.model.doc_hyper_class(self.base.name)

    def _encoded(self):
        return {
            'id_doc': "Integer",
            'nome_doc': "Text",
            'mimetype': "Text",
            'size': "Integer",
        }

    def __call__(self, value):
        """ @param value: string or dictionary, witch contains file id on disk, or not
            This method should return a dictonary in the form described by _encoded.
        """
        mask = None

        if value is None:
            return None

        if isinstance(value, str):
            if self.is_uuid(value):
                mask = self.build_file_mask(value)
            else:
                raise TypeError('Malformed mask: unrecognized pattern %s' % value)

        elif isinstance(value, dict):
            mask = self.get_file_mask(value)

            if self.is_uuid(mask.uuid):
                mask = self.build_file_mask(mask.uuid)
        else:
            raise TypeError('Malformed mask: Expected dict or str, but found %s' % type(value).__name__)

        assert(isinstance(mask, FileMask))

        return mask.__dict__

    def get_file_mask(self, value):
        if not value.get('size'): value['size'] = None
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
        file_name = base64.urlsafe_b64decode(file_name_encoded.encode('utf-8')).decode('utf-8')
        mime_type = '.'.join(split).replace('-', '/', 1)
        file_size = self.get_size(tmp_file)
        id_doc = self.entity.next_id()

        dt_ext_texto = None
        field_indices = [index.index for index in self.field.indices]
        if 'Nenhum' in field_indices:
            dt_ext_texto = datetime.datetime.now()

        self.base.__docs__[self.id].append({
           'id_doc': id_doc,
           'id_reg': self.id,
           'grupos_acesso': '',
           'nome_doc': file_name,
           'blob_doc': tmp_file.read(),
           'mimetype': mime_type,
           'texto_doc': None,
           'dt_ext_texto': dt_ext_texto
        })

        tmp_file.close()
        os.remove(tmp_file.name)

        return FileMask(id_doc, file_name, mime_type, file_size)

    def is_uuid(self, id):
        if id is None:
            return False
        try:
            uuid.UUID(id)
            return True
        except ValueError:
            return False

