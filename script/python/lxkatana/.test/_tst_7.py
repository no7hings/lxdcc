# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold', 'lxusd', 'lxshotgun',
        'lxutil', 'lxutil_gui',
        'lxkatana', 'lxkatana_gui'
    ]
)
p.set_reload()

import lxkatana_fnc.scripts as ktn_fnc_scripts

ktn_fnc_scripts.set_look_export_by_any_scene_file(
    '/l/prod/shl/publish/assets/chr/huotao/mod/td_test/huotao.mod.td_test.v002/huotao.katana'
)
