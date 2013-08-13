
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

                # Finally build group instance ...
                _group = Group(
                    name        = group_metadata['name'],
                    description = group_metadata['description'],
                    multivalued = Multivalued(group_metadata['multivalued']),
                    content     = assemble_content(group_content),
                )

                # ... and append it to content list
                content_list.append(_group)

            # ... Or do we have a field ?
            elif obj.get('field'):
                field = obj['field']

                # Build Field instance ...
                _field = Field(
                    name        = field['name'],
                    description = field['description'],
                    datatype    = DataType(field['datatype']),
                    indices     = [Index(i) for i in field['indices']],
                    multivalued = Multivalued(field['multivalued']),
                    required    = Required(field['required'])
                )

                # and append it to content list
                content_list.append(_field)

        return content_list

    _content = assemble_content(base_content)

    # build base instance
    base = Base(
        name            = base_metadata['name'],
        description     = base_metadata['description'],
        index_export    = base_metadata['index_export'],
        index_url       = base_metadata['index_url'],
        index_time      = base_metadata['index_time'],
        doc_extract     = base_metadata['doc_extract'],
        extract_time    = base_metadata['extract_time'],
        content         = _content
    )

    return base
