# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxobj', 'lxresolver',
        'lxarnold', 'lxusd', 'lxshotgun'
        'lxutil', 'lxutil_fnc', 'lxutil_gui',
        'lxmaya', 'lxmaya_fnc', 'lxmaya_gui',
        'publish'
    ]
)
p.set_reload()

import lxmaya_fnc.scripts as mya_fnc_scripts

mya_fnc_scripts.set_look_export_by_any_scene_file(
    '/l/prod/shl/publish/assets/chr/huotao/mod/td_test/huotao.mod.td_test.v002/scene/huotao.ma'
)
