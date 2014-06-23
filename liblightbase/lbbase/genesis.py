from liblightbase.lbbase.fields import *
from liblightbase.lbbase import Base


def json_to_base(base_json):

    """ Parses base_json and builds Base instance
    """
    base_metadata = base_json['metadata']
    base_content = base_json['content']
    structures = { }

    def assemble_content(content_object, dimension=0):

        """ Parses content object and builds a list with fields/groups instances
        """
        # Reserve return object
        content_list = list()

        # Parse object
        for obj in content_object:

            # Do we have a group ? ...
            if obj.get('group'):
                group_metadata = obj['group']['metadata']
                group_content = obj['group']['content']

                _dimension = dimension
                if group_metadata['multivalued'] is True:
                    _dimension = _dimension + 1

                # Build group instance ...
                _group = Group(
                    name = group_metadata['name'],
                    description = group_metadata['description'],
                    alias = group_metadata['alias'],
                    multivalued = Multivalued(group_metadata['multivalued']),
                    content = assemble_content(group_content, dimension=_dimension),
                )

                # ... and append it to content list
                content_list.append(_group)
                structures[_group.name] = _group

            # ... Or do we have a field ?
            elif obj.get('field'):
                field = obj['field']

                # Build indices list
                indices = field['indices']
                _indices = list()
                if type(indices) is list:
                    for index in indices:
                        _index = Index(index)
                        _indices.append(_index)

                # Finally Build Field instance ...
                _field = Field(
                    name = field['name'],
                    description = field['description'],
                    alias = field['alias'],
                    datatype = DataType(field['datatype']),
                    indices = _indices,
                    multivalued = Multivalued(field['multivalued']),
                    required = Required(field['required'])
                )
                if _field.multivalued:
                    _field.__dim__ = dimension + 1
                else:
                    _field.__dim__ = dimension

                # and append it to content list
                content_list.append(_field)
                structures[_field.name] = _field

        return content_list

    _content = assemble_content(base_content)

    # build base instance
    base = Base(
        name = base_metadata['name'],
        description = base_metadata['description'],
        password = base_metadata['password'],
        color = base_metadata['color'],
        id_base = base_metadata.get('id_base'),
        dt_base = base_metadata.get('dt_base'),
        idx_exp = base_metadata['idx_exp'],
        idx_exp_url = base_metadata['idx_exp_url'],
        idx_exp_time = base_metadata['idx_exp_time'],
        file_ext = base_metadata['file_ext'],
        file_ext_time = base_metadata['file_ext_time'],
        content = _content
    )

    base.__structs__ = structures
    return base
