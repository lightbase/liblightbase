#!/usr/bin/python
# -*- encoding: utf-8 -*-

from liblightbase.lbsearch.search import Collection

import requests

class ElasticSearch():
    def search(self, resourceURL, lbBaseInstance, jsonQuery, additionalParams={'fields': '_metadata.id_doc', 'lbquery': '1'}):

        baseName = lbBaseInstance.metadata.name
        completeURL = resourceURL + "/" + baseName + "/es/_search"


        # Note: Essa conversão para UTF-8 é necessária principalmente por causa 
        # dos caracteres latinos! By Questor
        jsonQueryUTF8 = jsonQuery.encode(encoding='UTF-8',errors='strict')

        headersForRequest = {'content-type': 'application/json'}
        response = requests.post(completeURL, 
            params=additionalParams, 
            data=jsonQueryUTF8, 
            headers=headersForRequest, 
            timeout=120)


        # Note: To debug! By Questor
        # print("response.json()")

        return Collection(lbBaseInstance, **response.json())

# {'status': 500, 'type': 'Exception', 'error_message': 'SearchError: (ProgrammingError) syntax error at or near ")"\nLINE 4: WHERE id_doc in (25,)) AS anon_1\n                            ^\n \'SELECT count(*) AS count_1 \\nFROM (SELECT lb_doc_db_reg_anot_teses.id_doc AS lb_doc_db_reg_anot_teses_id_doc, lb_doc_db_reg_anot_teses.document AS lb_doc_db_reg_anot_teses_document \\nFROM lb_doc_db_reg_anot_teses \\nWHERE id_doc in (25,)) AS anon_1\' {}', 'request': {'path': '/api/db_reg_anot_teses/es/_search', 'client_addr': '192.168.25.254', 'user_agent': 'python-requests/2.3.0 CPython/3.2.2 Linux/2.6.32-431.20.3.el6.x86_64', 'method': 'POST'}}

