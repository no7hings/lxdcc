# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxresolver.commands as rsv_commands

import lxmaya_fnc.scripts as mya_fnc_scripts

resolver = rsv_commands.get_resolver()

scene_src_file_path = '/l/prod/cjd/publish/assets/flg/cao_c_03_flg/srf/surfacing/cao_c_03_flg.srf.surfacing.v002/scene/cao_c_03_flg.katana'

rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)

mya_fnc_scripts.set_asset_scene_src_create(
    rsv_task_properties
)
