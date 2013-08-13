
from liblightbase.lbbase.fields import *
from liblightbase.lbbase. __init__2 import *

example = {
    'metadata':{
        'name':'base_name',
        'description': 'base_description',
        'index_export': 'index_export',
        'index_url': 'index_url',
        'index_time': 'index_time',
        'doc_extract': 'doc_extract',
        'extract_time': 'extract_time',
    },
    'structure':[
        {"id":1},
        {"id":2,"children":[
            {"id":3},
            {"id":5,"children":[
                {"id":6},
            ]},
            {"id":9},
        ]},
        {"id":11},
    ],
    'context':{
        '1':{
            'name': 'nome1',
            'description': 'descricao1',
            'datatype': 'AlfaNumerico',
            'multivalued': True,
            'required': True,
            'indices': [
                'Textual',
                'Vazio'
            ]
        },
        '2':{
            'name': 'nome2',
            'description': 'descricao2',
            'multivalued': False,
        },
        '3':{
            'name': 'nome3',
            'description': 'descricao3',
            'datatype': 'AlfaNumerico',
            'multivalued': False,
            'required': True,
            'indices': [
                'Textual',
                'Vazio'
            ]
        },
        '5':{
            'name': 'nome5',
            'description': 'descricao5',
            'multivalued': True,
        },
        '6':{
            'name': 'nome6',
            'description': 'descricao6',
            'datatype': 'AlfaNumerico',
            'multivalued': True,
            'required': True,
            'indices':[
                'Textual',
                'Vazio'
            ]
        },
        '9':{
            'name': 'nome9',
            'description': 'descricao9',
            'datatype': 'AlfaNumerico',
            'multivalued': False,
            'required': True,
            'indices': [
                'Textual',
                'Vazio'
            ]
        },
        '11':{
            'name': 'nome11',
            'description': 'descricao11',
            'datatype': 'AlfaNumerico',
            'multivalued': True,
            'required': True,
            'indices': [
                'Textual',
                'Vazio'
            ]
        }
    },
}




def create_base(prelude):

    """ Creates Base instance based on predefined object
    """
    metadata    = prelude['metadata']
    structure   = prelude['structure']
    context     = prelude['context']

    def parse_structure(_structure):

        _content_list = list()
        for node in _structure:

            node_id = node['id']
            node_context = context[str(node_id)]

            # Do we have a group ? ...
            if node.get('children'):
                _content = parse_structure(node['children'])
                group = Group(
                    name        = node_context['name'],
                    description = node_context['description'],
                    multivalued = Multivalued(node_context['multivalued']),
                    content     = _content,
                )
                _content_list.append(group)

            # ... Or do we have a field ?
            else:
                field = Field(
                    name        = node_context['name'],
                    description = node_context['description'],
                    datatype    = DataType(node_context['datatype']),
                    indices     = [Index(i) for i in node_context['indices']],
                    multivalued = Multivalued(node_context['multivalued']),
                    required    = Required(node_context['required'])
                )
                _content_list.append(field)

        return _content_list

    content = parse_structure(structure)

    base = Base(
        name            = metadata['name'],
        description     = metadata['description'],
        index_export    = metadata['index_export'],
        index_url       = metadata['index_url'],
        index_time      = metadata['index_time'],
        doc_extract     = metadata['doc_extract'],
        extract_time    = metadata['extract_time'],
        content         = content
    )

    return base


base = create_base(example)
print(base.json)
