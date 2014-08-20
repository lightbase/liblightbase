#!/usr/bin/python
# -*- encoding: utf-8 -*-

import requests

class ElasticSearch():
	def search(self, urlNParameters, jsonRequest):
		jsonRequestUTF8 = jsonRequest.encode(encoding='UTF-8',errors='strict')
		response = requests.post(urlNParameters, 
			data=jsonRequestUTF8, 
			timeout=120)
		return response.text

