# -*- coding: utf-8 -*-
from liblightbase.lbrest.core import LBRest
from liblightbase.lbutils.conv import document2json
from liblightbase.lbutils.conv import json2document
from liblightbase.lbbase.struct import Base
from liblightbase.lbsearch.search import Collection
from liblightbase.lbsearch.search import Search
from liblightbase import lbutils
from liblightbase.lbutils.conv import dict2genericbase

class DocumentREST(LBRest):

    """ 
    Contains methods for handling LightBase Files. The communicating is via 
    http to the LighBase REST API.
    """

    def __init__(self, rest_url, base, response_object=False):
        """
        Class constructor.
        @param rest_url: The REST URL.
        @param base: String or Base object.
        """
        super(DocumentREST, self).__init__(rest_url, response_object)
        msg = 'base must be a Base object.'
        assert isinstance(base, Base), msg
        self.base = base

    def get_collection(self, search_obj=None, instance=True, return_as_dict=False):
        """
        Retrieves collection of documents according to search object.
        @param search_obj: JSON which represents a search object.
        """
        if search_obj is not None:
            msg = 'search_obj must be a Search object.'
            assert isinstance(search_obj, Search), msg
        else:
            search_obj = Search()
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.doc_prefix],
            params={self.search_param: search_obj._asjson()})

        # NOTE: Adicionado pelo Bleno 06/10/2016. Adicionado por Bleno Nascimento 
        # Silva aproximadamente 2 anos atrás removendo a validação no retorno do método 
        # "get_collection". By Alexandre
        # return Collection(self.base, **lbutils.json2object(response))
        # return dict2genericbase(response.json())

        if return_as_dict:
            return dict2genericbase(lbutils.json2object(response))
        else:            
            return Collection(self.base, **lbutils.json2object(response))

    def update_collection(self, search_obj=None, path_list=[]):
        """
        Updates collection of documents according to search object.
        @param search_obj: JSON which represents a search object.
        """
        if search_obj is not None:
            msg = 'search_obj must be a Search object.'
            assert isinstance(search_obj, Search), msg
        else:
            search_obj = Search()
        response = self.send_request(self.httpput,
            url_path=[self.basename, self.doc_prefix],
            params={self.search_param: search_obj._asjson(),
            self.path_param: lbutils.object2json(path_list)})
        return response

    def get(self, id):
        """
        Retrieves document by id.
        @param id: The document identify.
        """
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.doc_prefix, str(id)])
        return json2document(self.base, response)

    def create(self, document):
        """
        Creates new document.
        @param document: Updated Document.
        """
        response = self.send_request(self.httppost,
            url_path=[self.basename, self.doc_prefix],
            data={self.doc_param: document})
        return int(response)

    def update(self, id, document):
        """
        Updates document by id.
        @param id: The document identify.
        @param document: Updated Document.
        """
        return self.send_request(self.httpput,
            url_path=[self.basename, self.doc_prefix, str(id)],
            data={self.doc_param: document})

    def delete(self, id):
        """
        Deletes document by id.
        @param id: The document identify.
        """
        return self.send_request(self.httpdelete,
            url_path=[self.base.metadata.name, self.doc_prefix, str(id)])

    def get_path(self, id, path):
        """
        Retrieves given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        """
        return self.send_request(self.httpget,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path))

    def create_path(self, id, path, value):
        """
        Creates given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        @param value: The value to create on path.
        """
        return self.send_request(self.httppost,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path),
            data={self.doc_param:value})

    def update_path(self, id, path, value):
        """
        Updates given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        @param value: The value to create on path.
        """
        return self.send_request(self.httpput,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path),
            data={self.doc_param:value})

    def delete_path(self, id, path):
        """
        Deletes given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        """
        return self.send_request(self.httpdelete,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path),
            data={self.doc_param:value})

