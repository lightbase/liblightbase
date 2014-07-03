def Property(func):
    """ Return a property with get and set.
        More information about this: 
        http://adam.gomaa.us/blog/2008/aug/11/the-python-property-builtin/
    """
    return property(**func()) 
    
def isiterable(obj,allow_string=True):
    """ Return if the argument is iterable
        Since a string is also an iterable, this function will return
        true when it's string. If allow_string is False
        strings will return False
    """
    if not allow_string and isinstance(obj, (str, unicode)):
        return False
    try: 
        it = iter(obj)
        return True
    except TypeError: 
        return False
