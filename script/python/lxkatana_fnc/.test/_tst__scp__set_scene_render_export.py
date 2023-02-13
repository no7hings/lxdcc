# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxresolver.commands as rsv_commands

import lxkatana_fnc.scripts as ktn_fnc_scripts

resolver = rsv_commands.get_resolver()
#
scene_file_path = '/l/prod/cjd/publish/assets/chr/huayao/srf/srf_cfxshading/huayao.srf.srf_cfxshading.v005/scene/huayao.katana'

ktn_fnc_scripts.set_render_export_by_any_scene_file(
    'file={}&td_enable=True'.format(scene_file_path)
)
