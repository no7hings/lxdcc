# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxresolver.commands as rsv_commands

import lxmaya_fnc.scripts as mya_fnc_scripts

resolver = rsv_commands.get_resolver()

scene_src_file_path = '/l/prod/cjd/publish/assets/flg/cao_c_03_flg/srf/surfacing/cao_c_03_flg.srf.surfacing.v002/scene/cao_c_03_flg.ma'

mya_fnc_scripts.set_scene_export_by_any_scene_file(
    'file={}&create_scene_src=True&with_scene=True&with_texture_tx=True'.format(scene_src_file_path)
)
