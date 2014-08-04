from liblightbase import lbutils
from liblightbase.lbbase.struct import Base
from liblightbase.lbbase.metadata import BaseMetadata
from liblightbase.lbbase.content import Content
from liblightbase.lbbase.lbstruct.field import Field
from liblightbase.lbbase.lbstruct.group import Group
from liblightbase.lbbase.lbstruct.group import GroupMetadata
from liblightbase import pytypes


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
                group_content = assemble_content(obj['group']['content'],
                    dimension=_dimension)
                group = Group(metadata = group_metadata,
                    content = group_content)
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
    if metaclass is None:
        metaclass = base.metaclass()
        if dictobj.get('_metadata'):
            dictobj.pop('_metadata')
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
        except AttributeError: pass
        else:
            if isinstance(value, property):
                continue
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
    :param obj: Python object
    :return: LBBase instance
    """
    base_metadata = dict(
            #id_base=1,
            name = getattr(type(obj), '__name__'),
            description = getattr(type(obj), '__name__'),
            password=None,
            idx_exp = False,
            #idx_exp_url = 'index_url',
            idx_exp_time=300,
            file_ext=True,
            file_ext_time=300,
            color='#FFFFFF'
        )

    content_list = Content()
    base_metadata = BaseMetadata(**base_metadata)

    attributes = lbutils.get_attr(obj)
    for elm in attributes:
        # Generate field object for every class attribute
        content_list.append(attribute2lbfield(elm))


    base = Base(
            metadata=base_metadata,
            content=content_list
        )

    return base


def attribute2lbfield(elm):
    """
    Convert object attributes to LB Field
    :param elm: Elm dictionary of attributes description
    :return: LB Field Object
    """
    #print(elm)
    # First theck if it's an object
    try:
        content_list = Content()
        for group_elm in elm['value'].__dict__.keys():
            # Now convert to field every group element
            dict_elm = {
                    'name': elm['name']+'_'+group_elm,
                    'type': type(elm['value'].__dict__.get(group_elm)),
                    'value': getattr(elm['value'], group_elm)
                }
            #print(group_elm)
            group_field = attribute2lbfield(dict_elm)
            content_list.append(group_field)

        group_metadata = dict(
            name = elm['name'],
            alias= elm['name'],
            description = elm['name'],
            multivalued = False
        )
        group_metadata = GroupMetadata(**group_metadata)

        group = Group(
            metadata=group_metadata,
            content=content_list,
        )
        return group
    except:
        # Now proccess field regularly
        if elm['type'] == dict:
            # Consider it a group
            content_list = Content()

            for group_elm in elm['value'].keys():
                # Now convert to field every group element
                dict_elm = {
                        'name': elm['name']+'_'+group_elm,
                        'type': type(elm['value'][group_elm]),
                        'value': elm['value'][group_elm]
                    }
                #print(group_elm)
                group_field = attribute2lbfield(dict_elm)
                content_list.append(group_field)

            group_metadata = dict(
                name = elm['name'],
                alias= elm['name'],
                description = elm['name'],
                multivalued = False
            )
            group_metadata = GroupMetadata(**group_metadata)

            group = Group(
                metadata=group_metadata,
                content=content_list,
            )
            return group

        elif elm['type'] == list:
            # Check for multivalued group
            lbtype = 'Text'
            if len(elm['value']) > 0:
                # Consider it a list
                lbtype = pytypes.pytype2lbtype(type(elm['value'][0]))
                #print(type(elm['value'][0]))
                #print(lbtype)
                if type(elm['value'][0]) == dict:
                    content_list = Content()
                    # Now convert to field every group element
                    for dict_key in elm['value'][0].keys():
                        dict_elm = {
                            'name': dict_key,
                            'type': type(elm['value'][0][dict_key]),
                            'value': elm['value'][0][dict_key]
                        }

                        group_field = attribute2lbfield(dict_elm)
                        content_list.append(group_field)

                    group_metadata = dict(
                        name = elm['name'],
                        alias= elm['name'],
                        description = elm['name'],
                        multivalued = True
                    )
                    group_metadata = GroupMetadata(**group_metadata)

                    group = Group(
                        metadata=group_metadata,
                        content=content_list,
                    )

                    return group


            field = dict(
                name = elm['name'],
                description = elm['name'],
                alias=elm['name'],
                datatype = lbtype,
                indices = ['Textual'],
                multivalued = True,
                required = True
            )

            field = Field(**field)
            return field
        else:
            lbtype = pytypes.pytype2lbtype(elm['type'])

            # Defaults to Text
            if lbtype is None:
                lbtype = 'Text'

            field = dict(
                name = elm['name'],
                description = elm['name'],
                alias=elm['name'],
                datatype = lbtype,
                indices = ['Textual'],
                multivalued = False,
                required = True
            )

            field = Field(**field)

            return field