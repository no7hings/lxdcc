# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold',
        'lxutil', 'lxutil_gui',
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
