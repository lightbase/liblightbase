# -*- coding: utf-8 -*-

from liblightbase.lbrest.file import FileREST

base_test = 'base_tree_lbdoc_test'

rest = FileREST('http://api.brlight.net/api', base_test)


with open('fiénâme.txt', 'r') as f:

    b = f.read()
    n = f.name
    
    print(n)
arq = open('fiénâme.txt', 'r')
resp = rest.create((arq))

print(resp)
