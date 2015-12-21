import requests

from liblightbase.lbsearch.search import Collection


class ElasticSearch():
    """ Trata-se de um proxy p/ o ES.
    """

    def search(self, resourceURL, lbBaseInstance, jsonQuery, additionalParams={'lbquery': '1'}):
        additionalParams = None;
        baseName = lbBaseInstance.metadata.name
        completeURL = resourceURL + "/" + baseName + "/es/_search"

        # Note: Essa conversão para UTF-8 é necessária principalmente 
        # por causa  dos caracteres latinos! By Questor
        jsonQueryUTF8 = jsonQuery.encode(encoding='UTF-8',errors='strict')

        headersForRequest = {'content-type': 'application/json'}
        response = requests.post(completeURL, 
            params=additionalParams, 
            data=jsonQueryUTF8, 
            headers=headersForRequest, 
            timeout=120)
        return response.json()