import sys

PY3 = sys.version_info[0] == 3

if PY3:
    PYSTR = str
else:
    PYSTR = basestring


RESERVED_STRUCT_NAMES = [

    # Reserved struct names from base's table. This names probrably won't be
    # reserved becuse they don't interfer at document's and file's tables.
    #'id_base',
    #'name',
    #'struct',
    #'dt_base',
    #'idx_exp',
    #'idx_exp_url',
    #'idx_exp_time',
    #'file_ext',
    #'file_ext_time',

    # Reserved struct names from document's table.
    'id_doc',
    'document',
    'dt_doc',
    'dt_last_up',
    'dt_del',
    'dt_idx',

    # Reserved struct names from file's table.
    'id_file',
    'id_doc',
    'filename',
    'file',
    'mimetype',
    'filesize',
    'filetext',
    'dt_ext_text',

    # Other restrictions.
    '_metadata',
    '__init__'
]
