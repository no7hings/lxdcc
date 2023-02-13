# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxresolver.commands as rsv_commands
#
import lxresolver.operators as rsv_operators

import lxkatana_fnc.scripts as ktn_fnc_scripts

resolver = rsv_commands.get_resolver()
#
scene_file_path = '/l/prod/cjd/publish/assets/chr/wuhu/srf/srf_anishading/wuhu.srf.srf_anishading.v001/scene/wuhu.katana'
#

rsv_task_properties_0 = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
version = rsv_task_properties_0.get('version')

surface_cfx_katana_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties_0).get_surface_cfx_katana_src_file(
    version=version
)

ktn_fnc_scripts.set_cfx_look_export_by_any_scene_file(
    'file={}&create_rsv_task=True'.format(surface_cfx_katana_scene_src_file_path)
)
