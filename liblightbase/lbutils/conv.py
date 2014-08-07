from liblightbase import lbutils
from liblightbase.lbbase.struct import Base
from liblightbase.lbbase.metadata import BaseMetadata
from liblightbase.lbbase.content import Content
from liblightbase.lbbase.lbstruct.field import Field
from liblightbase.lbbase.lbstruct.group import Group
from liblightbase.lbbase.lbstruct.group import GroupMetadata
from liblightbase import pytypes
from liblightbase.lbdoc.metadata import DocumentMetadata


def json2base(jsonobj):
    """
    Convert a JSON string to liblightbase.lbbase.struct.Base object.
    @param jsonobj: JSON string.
    """
    return dict2base(dictobj=lbutils.json2object(jsonobj))


def base2json(base):
    """
    Convert a liblightbase.lbbase.struct.Base object to JSON string.
    @param jsonobj: JSON string.
    """
    return base.json


def json2document(base, jsonobj):
    """
    Convert a JSON string to BaseMetaClass object.
    @param base: liblightbae.lbbase.Base object
    @param jsonobj: JSON string.
    """
    return dict2document(base=base, dictobj=lbutils.json2object(jsonobj))


def document2json(base, document, **kw):
    """
    Convert a BaseMetaClass object to JSON string.
    @param document: BaseMetaClass object
    """
    return lbutils.object2json(document2dict(base, document), **kw)


def dict2base(dictobj):
    """
    Convert dictionary object to Base object
    @param dictobj: dictionary object
    """
    def assemble_content(content_object, dimension=0):
        """
        Parses content object and builds a list with Field and Group objects
        @param content_object:
        @param dimension:
        """
        content_list = Content()
        for obj in content_object:
            if obj.get('group'):
                group_metadata = GroupMetadata(**obj['group']['metadata'])
                _dimension = dimension
                if group_metadata.multivalued:
                    _dimension += 1
                group_content = assemble_content(
                    obj['group']['content'],
                    dimension=_dimension)
                group = Group(
                    metadata=group_metadata,
                    content=group_content)
                content_list.append(group)
            elif obj.get('field'):
                field = Field(**obj['field'])
                if field.multivalued:
                    field.__dim__ = dimension + 1
                else:
                    field.__dim__ = dimension
                content_list.append(field)
        return content_list
    base = Base(metadata=BaseMetadata(**dictobj['metadata']),
        content=assemble_content(dictobj['content']))
    return base


def dict2document(base, dictobj, metaclass=None):
    """
    Convert a dictionary object to BaseMetaClass object.
    @param base: Base object.
    @param dictobj: dictionary object.
    @param metaclass: GroupMetaClass in question.
    """
    kwargs = {}
    if metaclass is None:
        metaclass = base.metaclass()
        if dictobj.get('_metadata'):
            kwargs['_metadata'] = DocumentMetadata(**dictobj.pop('_metadata'))
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
                        metaclass=base.metaclass(struct.metadata.name))
                    meta_object.append(meta_inner_object)
            else:
                meta_object = dict2document(
                    base=base,
                    dictobj=dictobj[member],
                    metaclass=base.metaclass(struct.metadata.name))
            kwargs[member] = meta_object
    return metaclass(**kwargs)


def document2dict(base, document, struct=None):
    """
    Convert a BaseMetaClass object to dictionary object.
    @param base: Base object.
    @param document: BaseMetaClass object
    @param struct: Field or Group object 
    """
    dictobj = { }
    if not struct: snames = base.content.__snames__
    else: snames = struct.content.__snames__
    for sname in snames:
        try: value = getattr(document, sname)
        except AttributeError:
            pass
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


def pyobject2base(obj):
    """
    Convert python object to base
    @param obj: Python object
    @return: LBBase instance
    """
    content = Content()
    elms = lbutils.get_attr(obj)
    for elm in elms:
        content.append(attribute2lbfield(*elm))
    return Base(
        metadata=BaseMetadata(getattr(type(obj), '__name__')),
        content=content)


def attribute2lbfield(attr_name, attr_type, attr_value):
    """
    Convert object attributes to LB Field
    @param elm: Elm dictionary of attributes description
    @return: LB Field Object
    """

    try:
        content_list = Content()
        for group_elm in attr_value.__dict__.keys():
            # Now convert to field every group element
            content_list.append(attribute2lbfield(
                #attr_name + '_' + group_elm,
                group_elm,
                type(attr_value.__dict__.get(group_elm)),
                getattr(attr_value, group_elm)))
        group_metadata = GroupMetadata(
            name=attr_name,
            alias=attr_name,
            description=attr_name,
            multivalued=False)
        return Group(
            metadata=group_metadata,
            content=content_list)
    except:
        # Now proccess field regularly
        if attr_type == dict:
            # Consider it a group
            content_list = Content()
            for group_elm in attr_value.keys():
                content_list.append(attribute2lbfield(
                    #attr_name + '_' + group_elm,
                    group_elm,
                    type(attr_value[group_elm]),
                    attr_value[group_elm]))
            group_metadata = GroupMetadata(
                name=attr_name,
                alias=attr_name,
                description=attr_name,
                multivalued = False)
            return Group(
                metadata=group_metadata,
                content=content_list)

        elif attr_type == list:
            # Check for multivalued group
            lbtype = 'Text'
            if len(attr_value) > 0:
                lbtype = pytypes.pytype2lbtype(type(attr_value[0]))
                #print(type(attr_value[0]))
                try:
                    content_list = Content()
                    for group_elm in attr_value[0].__dict__.keys():
                        # Now convert to field every group element
                        content_list.append(attribute2lbfield(
                            #attr_name + '_' + group_elm,
                            group_elm,
                            type(attr_value[0].__dict__.get(group_elm)),
                            getattr(attr_value[0], group_elm)))
                    group_metadata = GroupMetadata(
                        name=attr_name,
                        alias=attr_name,
                        description=attr_name,
                        multivalued=True)
                    return Group(
                        metadata=group_metadata,
                        content=content_list)
                except:
                    # Now proccess field regularly
                    if type(attr_value[0]) == dict:
                        # Consider it a group
                        content_list = Content()
                        for group_elm in attr_value[0].keys():
                            content_list.append(attribute2lbfield(
                                #attr_name + '_' + group_elm,
                                group_elm,
                                type(attr_value[0][group_elm]),
                                attr_value[0][group_elm]))
                        group_metadata = GroupMetadata(
                            name=attr_name,
                            alias=attr_name,
                            description=attr_name,
                            multivalued = True)
                        return Group(
                            metadata=group_metadata,
                            content=content_list)

            #print(lbtype)
            return Field(
                name=attr_name,
                description=attr_name,
                alias=attr_name,
                datatype = lbtype,
                indices = ['Textual'],
                multivalued = True,
                required = True)
        else:
            return Field(
                name=attr_name,
                description=attr_name,
                alias=attr_name,
                datatype = pytypes.pytype2lbtype(attr_type) or 'Text',
                indices = ['Textual'],
                multivalued = False,
                required = True)
