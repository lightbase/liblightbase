# -*- coding: utf-8 -*-
from liblightbase.lbrest.core import LBRest
import os
import uuid

class FileREST(LBRest):

    """
    Contains methods for handling LightBase documents. The communicating is via 
    http to the LighBase REST API.
    """

    def __init__(self, rest_url, base):
        """
        Class constructor.
        @param rest_url: The REST URL.
        @param base: String or Base object.
        """
        super(REST, self).__init__(rest_url)
        self.base = base

    def get(id, sys_dir='/tmp'):
        """
        Retrieves file by id, returning file headers and file path on local 
        file system. 
        @param id: The file identify.
        @param sys_dir: The file identify.
        """
        filepath = os.path.join(sys_dir, str(uuid.uuid4()))
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix, str(id), 'download'],
            stream=True)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return self.get_file_headers(response), filepath

    def get_file_headers(self, response):
        cd = response.headers['Content-Disposition']
        return {
            'filename': cd[cd.rfind("=") + 1:].strip(),
            'mimetype': response.headers['Content-Type']
        }

    def download(id, sys_dir):
        """ Alias to @method get 
        """
        return self.get(id, sys_dir)

    def create(files):
        """
        Creates files.
        @param files:
        """
        return self.send_request(self.httppost,
            url_path=[self.basename, self.file_prefix, str(id)],
            files=files)

    def upload(self, files):
        """ Alias to @method create
        """
        return self.create(files)

    def update():
        """
        """
        pass

    def delete():
        """
        """
        pass
