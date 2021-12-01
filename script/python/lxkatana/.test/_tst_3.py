# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxobj', 'lxresolver',
        'lxarnold',
        'lxutil', 'lxutil_gui',
        'lxkatana', 'lxkatana_gui'
    ]
)
p.set_reload()

import lxkatana.dcc.dcc_operators as ktn_dcc_operators

geometry_file_path, hair_file_path, look_file_path, katana_look_file_path, source_katana_file_path = [
    '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/geometry/scene/v009/hi.abc',
    None,
    '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v009/all.ass',
    None,
    None
]
