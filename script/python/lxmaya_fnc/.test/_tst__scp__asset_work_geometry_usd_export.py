# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxresolver.commands as rsv_commands

import lxmaya_fnc.scripts as mya_fnc_scripts

import lxusd_fnc.scripts as usd_fnc_scripts


r = rsv_commands.get_resolver()

scene_src_file_path = '/l/prod/lib/work/assets/chr/ast_cjd_didi/srf/surfacing/maya/scenes/ast_cjd_didi.srf.surfacing.v001.ma'

rsv_task_properties = r.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)

mya_fnc_scripts.set_asset_work_geometry_usd_export(rsv_task_properties)

usd_fnc_scripts.set_asset_work_geometry_uv_map_usd_export(
    rsv_task_properties
)
