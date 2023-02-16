# coding:utf-8
from lxutil import utl_core

import lxresolver.commands as rsv_commands

from lxdeadline import ddl_core

import lxdeadline.methods as ddl_methods

import lxdeadline.objects as ddl_objects
#
utl_core.Environ.set_td_enable(True)

assets = [
    # u'huayao',
    # u'laohu_xiao',
    # u'nn_gongshifu',
    u'qunzhongnv_b',
    # u'td_test',
    # u'wuhu'
]

resolver = rsv_commands.get_resolver()

rsv_project = resolver.get_rsv_project(project='cjd')

user = utl_core.System.get_user_name()
time_tag = utl_core.System.get_time_tag()

for i_asset in assets:
    i_rsv_task = rsv_project.get_rsv_task(asset=i_asset, task='surfacing')
    i_katana_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
    i_katana_scene_src_file_path = i_katana_scene_src_file_unit.get_result()
    if i_katana_scene_src_file_path:
        i_rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=i_katana_scene_src_file_path)
        #
        i_shotgun_render_export_query = ddl_objects.DdlRsvTaskQuery(
            'shotgun-render-export', i_rsv_task_properties
        )
        print i_shotgun_render_export_query.get_method_option()
        #
        i_katana_look_checker_export_runner = ddl_methods.RsvTaskHookExecutor(
            method_option=i_shotgun_render_export_query.get_method_option(),
            script_option=i_shotgun_render_export_query.get_script_option(
                file=i_katana_scene_src_file_path,
                with_asset_info=True,
                with_look_pass_info=True,
                td_enable=True,
                #
                user=user, time_tag=time_tag,
            )
        )
        i_katana_look_checker_export_runner.execute_with_deadline()
