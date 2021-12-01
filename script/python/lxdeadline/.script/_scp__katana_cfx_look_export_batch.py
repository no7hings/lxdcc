# coding:utf-8
from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxdeadline.objects as ddl_objects

import lxdeadline.methods as ddl_methods
#
utl_core.Environ.set_td_enable(True)

assets = [
    'didi',
]

resolver = rsv_commands.get_resolver()

rsv_project = resolver.get_rsv_project(project='cjd')

user = utl_core.System.get_user_name()
time_tag = utl_core.System.get_time_tag()

for i_asset in assets:
    i_rsv_task = rsv_project.get_rsv_task(asset=i_asset, task='srf_cfxshading')
    i_katana_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
    i_katana_scene_src_file_path = i_katana_scene_src_file_unit.get_result()
    if i_katana_scene_src_file_path:
        i_rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=i_katana_scene_src_file_path)
        #
        i_export_query = ddl_objects.DdlRsvTaskQuery(
            'katana-cfx-look-export', i_rsv_task_properties
        )
        i_export = ddl_methods.DdlRsvTaskMethodRunner(
            method_option=i_export_query.get_method_option(),
            script_option=i_export_query.get_script_option(
                file=i_katana_scene_src_file_path,
                create_scene_src=True,
                with_scene=True,
                with_texture=True,
                #
                user=user, time_tag=time_tag,
                #
                td_enable=True
            )
        )
        i_export.set_run_with_deadline()

