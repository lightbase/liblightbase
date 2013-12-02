
from liblightbase.lbutils import reify
from liblightbase.lbutils import FileMask
from liblightbase.lbutils import is_uuid
from liblightbase.lbtypes import BaseDataType
import lbgenerator
import glob
import os
import base64

class FileExtension(BaseDataType):

    """ Represents an extension for file-based Fields
    """
    def __init__(self, base, field, id):
        super(FileExtension, self).__init__(base, field, id)
        self.tmp_dir = lbgenerator.config.TMP_DIR + '/lightbase_tmp_storage/' + self.base.name
        self.entity = lbgenerator.model.doc_hyper_class(self.base.name)

    def __call__(self, value):
        if value == '' or value is None:
            return value
        file_mask = self.get_file_mask(value)
        if not file_mask:
            raise Exception(
                """
                    File mask must be like following json format: 
                    {
                        "id_doc":"",
                        "nome_doc":"",
                        "mimetype":"",
                        "uuid":"",
                    }'
                """
            )
        if file_mask['uuid'] and is_uuid(file_mask['uuid']):
            file_mask = self.build_file_mask(file_mask['uuid'])
        return file_mask

    def get_file_mask(self, value):
        try: return FileMask(**dict(value)).__dict__
        except: return False

    def build_file_mask(self, value):
        tmp_file = self.find_tmp_file(value)
        if tmp_file:
            return self.save_file(tmp_file).__dict__
        else:
            raise Exception('Could not find temporary file %s on disk' % value)

    def find_tmp_file(self, uuid):
        tmp_file = None
        for file_path in glob.glob(self.tmp_dir + '/' + uuid + '*'):
            tmp_file = open(file_path, 'rb')
        return tmp_file

    def save_file(self, tmp_file):
        fake_name = os.path.split(tmp_file.name)[1]
        split = fake_name.split('.')

        uuid = split.pop(0)
        file_name_encoded = split.pop()
        file_name = base64.urlsafe_b64decode(file_name_encoded.encode('utf-8')).decode('utf-8')
        mime_type = '.'.join(split).replace('-', '/', 1)
        id_doc = self.entity.next_id()

        self.base.__docs__[self.id].append({
           'id_doc': id_doc,
           'id_reg': self.id,
           'grupos_acesso': '',
           'nome_doc': file_name,
           'blob_doc': tmp_file.read(),
           'mimetype': mime_type,
           'texto_doc': None,
           'dt_ext_texto': None
        })

        tmp_file.close()
        #os.remove(tmp_file.name)

        return FileMask(id_doc, file_name, mime_type, None)

