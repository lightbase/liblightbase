#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import datetime

JSON_TYPES = (
    dict,        # object
    list,        # array
    int,         # number (int)
    float,       # number (float)
    bool,        # true, false
    type(None)   # null
)


# ********************************** 
# * Document default encode/decode *
# ********************************** 

class DocumentJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        """Convert ``obj`` to something JSON encoder can handle."""

        if isinstance(obj, datetime.datetime):
            obj = obj.strftime('%d/%m/%Y %H:%M:%S')

        elif isinstance(obj, datetime.time):
            obj = obj.strftime('%H:%M:%S')

        elif isinstance(obj, datetime.date):
            obj = obj.strftime('%d/%m/%Y')

        else:
            # method to generate JSON
            obj = obj._encoded()

        return obj

# ************************
# * Generic JSON encoder *
# ************************

def object2json(value, ensure_ascii=False, **kwargs):
    """ @param value: Python object  to convert into JSON
        @param ensure_ascii: The output is guaranteed to have all incoming 
        non-ASCII characters escaped. Defaults to False 
        @param kwargs: key word arguments that will be used with Python's JSON 
        standard library

        This method receives a Python object JSON oject and tries to convert it
        to JSON oject. 
    """
    return json.dumps(value,
                     ensure_ascii=ensure_ascii,
                     cls=DocumentJSONEncoder,
                     **kwargs)

# ************************ 
# * Generic JSON decoder * 
# ************************ 

def json2object(value, **kwargs):
    """ @param value: JSON to convert into Python object
        @param kwargs: key word arguments that will be used with Python's JSON 
        standard library

        This method receives a JSON oject and tries to convert it to Python 
        object.
    """
    if isinstance(value, JSON_TYPES):
        # No need to parse, if it's already a JSON type
        return value
    else:
        # We do have a JSON that must have to transform it on a Python object
        try:
            # Loads JSON and return object
            # raw_decode method is used because of compatibility problems.
            return json.JSONDecoder(**kwargs).raw_decode(value)[0]

        except Exception as e:
            # JSON loading was not possible
            raise e.__class__('Could not parse JSON data: %s' % e)
