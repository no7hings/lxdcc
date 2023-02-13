# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxresolver.commands as rsv_commands

import lxshotgun_fnc.scripts as stg_fnc_scripts

resolver = rsv_commands.get_resolver()
#
scene_file_path = '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/scene/qunzhongnv_b.katana'

stg_fnc_scripts.set_render_export_by_any_scene_file(
    'file={}&with_look_pass_info=True&with_asset_info=True&td_enable=True'.format(scene_file_path)
)
