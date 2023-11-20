# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold',
        'lxutil',
        'lxkatana', 'lxkatana_gui'
    ]
)
p.set_reload()

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

texture_references = ktn_dcc_objects.TextureReferences().get_objs()
#
repath_list = []
convert_list = []
if texture_references:
    for obj in texture_references:
        for port_path, file_path in obj.reference_raw.items():
            texture = utl_dcc_objects.OsFile(file_path)
            print obj, port_path, file_path
