from liblightbase import lbutils

def json2document(base, jsonobj):
    """
    Convert a JSON string to BaseMetaClass object.
    @param base: liblightbae.lbbase.Base object
    @param jsonobj: JSON string or dictionary.
    """
    return dict2document(base=base, dictobj=lbutils.json2object(jsonobj))

def dict2document(base, dictobj, metaclass=None):
    """
    Convert a dictionary object to BaseMetaClass object.
    @param dictobj: JSON string or dictionary.
    @param metaclass: GroupMetaClass in question.
    """
    if metaclass is None:
        metaclass = base.metaclass()
    kwargs = { }
    for member in dictobj:
        struct = base.get_struct(member)
        if struct.is_field:
            kwargs[member] = dictobj[member]
        elif struct.is_group:
            if struct.metadata.multivalued:
                meta_object = []
                for element in dictobj[member]:
                    meta_inner_object = dict2document(
                        base=base,
                        dictobj=element,
                        metaclass=base.get_metaclass(struct.metadata.name))
                    meta_object.append(meta_inner_object)
            else:
                meta_object = dict2document(
                    base=base,
                    dictobj=dictobj[member],
                    metaclass=base.get_metaclass(struct.metadata.name))
            kwargs[member] = meta_object
    return metaclass(**kwargs)

def document2json(base, document, **kw):
    """
    Convert a BaseMetaClass object to JSON string.
    @param document: BaseMetaClass object
    """
    return lbutils.object2json(document2dict(base, document), **kw)

def document2dict(base, document, struct=None):
    """
    Convert a BaseMetaClass object to dictionary object.
    @param document: BaseMetaClass object
    @param struct: Field or Group object 
    """
    dictobj = { }
    if not struct: snames = base.content.__snames__
    else: snames = struct.content.__snames__
    for sname in snames:
        try: value = getattr(document, sname)
        except AttributeError: pass
        else:
            _struct = base.get_struct(sname)
            if _struct.is_field:
                dictobj[sname] = value
            elif _struct.is_group:
                if _struct.metadata.multivalued:
                    _value = [ ]
                    for element in value:
                        _value.append(document2dict(
                            base=base,
                            document=element,
                            struct=_struct))
                else:
                    _value = document2dict(
                        base=base,
                        document=value,
                        struct=_struct)
                dictobj[sname] = _value
    return dictobj

