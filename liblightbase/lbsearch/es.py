#!/usr/bin/python
# -*- encoding: utf-8 -*-

import requests

class ElasticSearch():
	def search(self, urlNParameters, jsonRequest):

		# dataTest = {"eventType": jsonRequestUTF8, "fields": "_metadata.id_doc"}
		paramsTest = {"fields": "_metadata.id_doc"}

		jsonRequestUTF8 = jsonRequest.encode(encoding='UTF-8',errors='strict')
		response = requests.post(urlNParameters, 
			params=paramsTest, 
			data=jsonRequestUTF8, 
			timeout=120)
		return response.text

