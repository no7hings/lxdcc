# coding:utf-8
from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxdeadline.objects as ddl_objects

import lxdeadline.methods as ddl_methods

assets = [
    u'huayao',
    u'laohu_xiao',
    u'nn_gongshifu',
    u'qunzhongnv_b',
    u'td_test',
    u'wuhu',
    'qunzhongnan_c',
    'qunzhongnv_d',
    'huayao',
    'qunzhongnan_d',
    'didi',
    'jiejie',
    'denglong_a',
    'e10440_wuyan',
]

resolver = rsv_commands.get_resolver()

rsv_project = resolver.get_rsv_project(project='cjd')

user = utl_core.System.get_user_name()
time_tag = utl_core.System.get_time_tag()

rsv_entities = rsv_project.get_rsv_entities(role='chr')

for i_rsv_entity in rsv_entities:
    i_rsv_task = i_rsv_entity.get_rsv_task(step='srf', task='surfacing')
    if i_rsv_task:
        i_katana_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
        i_katana_scene_src_file_path = i_katana_scene_src_file_unit.get_result()
        #
        i_render_katana_scene_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-render-katana-scene-file')
        i_render_katana_scene_file_path = i_render_katana_scene_file_unit.get_result()
        if i_render_katana_scene_file_path is None:
            if i_katana_scene_src_file_path:
                i_rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
                    file_path=i_katana_scene_src_file_path)
                #
                i_export_query = ddl_objects.DdlRsvTaskQuery(
                    'katana-render-export', i_rsv_task_properties
                )
                i_export = ddl_methods.RsvTaskHookExecutor(
                    method_option=i_export_query.get_method_option(),
                    script_option=i_export_query.get_script_option(
                        file=i_katana_scene_src_file_path,
                        create_camera=True,
                        create_scene=True,
                        create_render=True,
                        #
                        with_shotgun_render=True,
                        width=1024, height=1024,
                        #
                        td_enable=False,
                        #
                        user=user, time_tag=time_tag
                    )
                )
                i_export.set_run_with_deadline()
