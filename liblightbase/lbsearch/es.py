#!/usr/bin/python
# -*- encoding: utf-8 -*-

import requests

class ElasticSearch():
	def search(self, resourceURL, baseName, jsonQuery, additionalParams={'fields': '_metadata.id_doc'}):
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
		return response.text

