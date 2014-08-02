# -*- coding: utf-8 -*-
from liblightbase.lbrest.core import LBRest
from liblightbase.lbutils.conv import document2json
from liblightbase.lbutils.conv import json2document
from liblightbase.lbbase.struct import Base
from liblightbase.lbsearch.search import Collection
from liblightbase.lbsearch.search import Search
from liblightbase import lbutils

class DocumentREST(LBRest):

    """ 
    Contains methods for handling LightBase Files. The communicating is via 
    http to the LighBase REST API.
    """

    def __init__(self, rest_url, base):
        """
        Class constructor.
        @param rest_url: The REST URL.
        @param base: String or Base object.
        """
        super(DocumentREST, self).__init__(rest_url)
        msg = 'base must be a Base object.'
        assert isinstance(base, Base), msg
        self.base = base

    def get_collection(self, search_obj=None):
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
            data={self.search_param: search_obj._asjson()})
        return Collection(self.base, **lbutils.json2object(response))

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

    def update(id, document):
        """
        Updates document by id.
        @param id: The document identify.
        @param document: Updated Document.
        """
        return self.send_request(self.httpput,
            url_path=[self.basename, self.doc_prefix, str(id)],
            data={self.doc_param: document})

    def delete(id):
        """
        Deletes document by id.
        @param id: The document identify.
        """
        return self.send_request(self.httpdelete,
            url_path=[self.base.metadata.name, self.doc_prefix, str(id)])

    def get_path(id, path):
        """
        Retrieves given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        """
        return self.send_request(self.httpget,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path))

    def create_path(id, path, value):
        """
        Creates given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        @param value: The value to create on path.
        """
        return self.send_request(self.httppost,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path),
            data={self.doc_param:value})

    def update_path(id, path, value):
        """
        Updates given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        @param value: The value to create on path.
        """
        return self.send_request(self.httpput,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path),
            data={self.doc_param:value})

    def delete_path(id, path):
        """
        Deletes given path on document.
        @param id: The document identify.
        @param path: List of structure names which form the path.
        """
        return self.send_request(self.httpdelete,
            url_path=(self.basename, self.doc_prefix, str(id))+tuple(path),
            data={self.doc_param:value})

