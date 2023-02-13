# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxobj', 'lxresolver',
        'lxarnold', 'lxusd', 'lxshotgun',
        'lxutil', 'lxutil_gui',
        'lxkatana', 'lxkatana_fnc', 'lxkatana_gui'
    ]
)
p.set_reload()

import lxkatana_fnc.scripts as ktn_fnc_scripts

ktn_fnc_scripts.set_look_export_by_any_scene_file(
    'file=/l/prod/shl/publish/assets/chr/huotao/mod/td_test/huotao.mod.td_test.v002/scene/huotao.katana'
)
