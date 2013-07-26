
from liblightbase.lbbase.fields import *
from liblightbase.lbbase. __init__2 import *
import json

def json_to_base(base_json):

    """ Parses base_json and builds Base instance
    """
    base_object = json.loads(base_json.encode('utf-8'))
    base_metadata = base_object['metadata']
    base_content = base_object['content']

    def assemble_content(content_object):

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

                # Build multivalued instance
                multivalued = group_metadata['multivalued']
                _multivalued = Multivalued(multivalued)

                # Build inner fields/groups
                _content_list = assemble_content(group_content)

                # Finally build group instance ...
                _group = Group(
                    name = group_metadata['name'],
                    description = group_metadata['description'],
                    content = _content_list,
                    multivalued = _multivalued
                )

                # ... and append it to content list
                content_list.append(_group)

            # ... Or do we have a field ?
            elif obj.get('field'):
                field = obj['field']

                # Build datatype instance
                datatype = field['datatype']
                _datatype = DataType(datatype)

                # Build indices list
                indices = field['indices']
                _indices = list()
                if type(indices) is list:
                    for index in indices:
                        _index = Index(index)
                        _indices.append(_index)

                # Build multivalued instance
                multivalued = field['multivalued']
                _multivalued = Multivalued(multivalued)

                # Finally Build Field instance ...
                _field = Field(
                    name = field['name'],
                    description = field['description'],
                    datatype = _datatype,
                    indices = _indices,
                    multivalued = _multivalued
                )

                # and append it to content list
                content_list.append(_field)

        return content_list

    _content = assemble_content(base_content)

    # build base instance
    base = Base(
        name = base_metadata['name'],
        description = base_metadata['description'],
        content = _content
    )

    return base
