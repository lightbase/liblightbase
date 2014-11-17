# -*- coding: utf-8 -*-
from liblightbase.lbrest.core import LBRest
import os
import uuid

class FileREST(LBRest):

    """
    Contains methods for handling LightBase documents. The communicating is via
    http to the LighBase REST API.
    """

    def __init__(self, rest_url, base, response_object=False):
        """
        Class constructor.
        @param rest_url: The REST URL.
        @param base: String or Base object.
        """
        super(FileREST, self).__init__(rest_url, response_object)
        self.base = base

    def get(self, id):
        """
        Retrieves file by id, returning file headers and file path on local 
        file system. 
        @param id: The file identify.
        """
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix, str(id), 'download'],
            stream=True)
        binary = response.content
        return self.get_file_headers(response), binary

    def get_path(self, id, path):
        """
        Retrieves a file attribute by id.
        @param id: The file identify.
        @param path: The file attribute to retrieve. Possible values are:
            -filetext;
            -filesize;
            -filename;
            -mimetype;
            -id_doc;
            -id_file;
            -dt_ext_text
        """
        return self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix, str(id), path])

    def get_file_headers(self, response):
        cd = response.headers['Content-Disposition']
        return {
            'filename': cd[cd.rfind("=") + 1:].strip(),
            'mimetype': response.headers['Content-Type']
        }

    def download(self, id):
        """ Alias to @method get 
        """
        return self.get(id)

    def create(self, files):
        """
        Creates files.
        @param files:('name.txt','\04nx\0content\nfile')}
        """
        return self.send_request(self.httppost,
            url_path=[self.basename, self.file_prefix],
            files={self.file_param : files})

    def upload(self, files):
        """ 
        Alias to @method create
        @param files type: tuple
        @param files: ('name.txt','content\nbinary\nfile')
        """
        return self.create(files)

    def update(self):
        """
        """
        pass

    def delete(self):
        """
        """
        pass
