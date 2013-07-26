example = {
    'metadata':{
        'name':'base_name',
        'description': 'base_description'
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
            'indices': [
                'Textual',
                'Vazio'
            ]
        }
        '2':{
            'name': 'nome9',
            'description': 'descricao9',
            'multivalued': False,
        }
        '3':{
            'name': 'nome3',
            'description': 'descricao3',
            'datatype': 'AlfaNumerico',
            'multivalued': False,
            'indices': [
                'Textual',
                'Vazio'
            ]
        }
        '5':{
            'name': 'nome9',
            'description': 'descricao9',
            'multivalued': True,
        }
        '6':{
            'name': 'nome6',
            'description': 'descricao6',
            'datatype': 'AlfaNumerico',
            'multivalued': True,
            'indices':
                'Textual',
                'Vazio'
            ]
        }
        '9':{
            'name': 'nome9',
            'description': 'descricao9',
            'datatype': 'AlfaNumerico',
            'multivalued': False,
            'indices': [
                'Textual',
                'Vazio'
            ]
        }
        '11':{
            'name': 'nome11',
            'description': 'descricao11',
            'datatype': 'AlfaNumerico',
            'multivalued': True,
            'indices': [
                'Textual',
                'Vazio'
            ]
        }
    },
}
