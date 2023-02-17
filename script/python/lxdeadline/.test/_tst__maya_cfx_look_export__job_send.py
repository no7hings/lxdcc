# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxresolver.commands as rsv_commands
#
import lxresolver.operators as rsv_operators

import lxdeadline.objects as ddl_objects

import lxdeadline.methods as ddl_methods

resolver = rsv_commands.get_resolver()
#
scene_file_path = '/l/prod/cjd/publish/assets/chr/nn_gongshifu/srf/srf_anishading/nn_gongshifu.srf.srf_anishading.v003/scene/nn_gongshifu.ma'
#
rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)

user = utl_core.System.get_user_name()
time_tag = utl_core.System.get_time_tag()

version = rsv_task_properties.get('version')

surface_cfx_katana_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_surface_cfx_katana_src_file(
    version=version
)
utl_dcc_objects.OsFile(surface_cfx_katana_scene_src_file_path).create_directory()
katana_cfx_look_export_query = ddl_objects.DdlRsvTaskQuery(
    'katana-cfx-look-export'
)
katana_cfx_look_export = ddl_methods.RsvTaskHookExecutor(
    method_option=katana_cfx_look_export_query.get_method_option(),
    script_option=katana_cfx_look_export_query.get_script_option(
        file=surface_cfx_katana_scene_src_file_path,
        create_rsv_task=True,
        #
        user=user, time_tag=time_tag,
    )
)
katana_cfx_look_export.execute_with_deadline()
