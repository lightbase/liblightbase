
from liblightbase.lbbase.struct import Base
from liblightbase.lbbase.metadata import BaseMetadata
from liblightbase.lbbase.content import Content
from liblightbase.lbbase.lbstruct.field import Field
from liblightbase.lbbase.lbstruct.group import Group
from liblightbase.lbbase.lbstruct.group import GroupMetadata

def json_to_base(base_json):

    """ Parses base json and return Base instance
    """

    # structures:  
    structures = { }

    def assemble_content(content_object, dimension=0):

        """ Parses content object and builds a list with fields/groups instances
        """

        # Reserve return object
        content_list = Content()

        # Parse object
        for obj in content_object:

            # Do we have a group ? ...
            if obj.get('group'):

                group_metadata = GroupMetadata(**obj['group']['metadata'])

                _dimension = dimension
                if group_metadata.multivalued:
                    _dimension = _dimension + 1

                group_content = assemble_content(obj['group']['content'],
                        dimension=_dimension)

                # Build group instance ...
                group = Group(
                    metadata = group_metadata,
                    content = group_content
                )

                if group.metadata.name not in structures:
                    structures[group.metadata.name] = group
                else:
                    raise NameError('Duplicated struct name: %s'\
                        % group.metadata.name)

                # ... and append it to content list
                content_list.append(group)

            # ... Or do we have a field ?
            elif obj.get('field'):

                # Assemble Field instance ...
                field = Field(**obj['field'])

                if field.multivalued:
                    field.__dim__ = dimension + 1
                else:
                    field.__dim__ = dimension

                # and append it to content list
                content_list.append(field)

                if field.name not in structures:
                    structures[field.name] = field
                else:
                    raise NameError('Duplicated struct name: %s'\
                        % field.name)

        return content_list

    base_metadata = base_json['metadata']
    base_content = assemble_content(base_json['content'])

    # build base instance
    base = Base(
        metadata=BaseMetadata(**base_metadata),
        content=base_content
    )

    base.__structs__ = structures
    return base
