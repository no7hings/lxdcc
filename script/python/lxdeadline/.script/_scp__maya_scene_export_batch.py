# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxdeadline.objects as ddl_objects

import lxdeadline.methods as ddl_methods

assets = [
    # 'taohuashu_b',
    # 'taohuashu_b',
    # 'yinghuashu_b',
    # 'taohuashu_gai',
    # 'yinghuashu_a',
    # 'e10440_wuyan',
    # 'zhujie_jiuguan',
    # 'zhujie_fuzhuangdian_a',
    # 'zhujie_fandian_a',
    # 'zhujie_tangguodian',
    # 'zhujie_zixunchu',
    # 'zhujie_binguan',
    # 'zhujie_denglongdian',
    # 'zhujie_lipindian_a',
    # 'shoushihe',
    # 'denglong_f',
    # 'diaopai_a',
    # 'guashi',
    # 'tanwei_h',
    # 'denglong_k',
    # 'tanwei_g',
    # 'denglong_g',
    # 'tanwei_i',
    # 'xiaodenglong_a',
    # 'denglong_cai',
    # 'denglong_d',
    'taohuashu',
]

resolver = rsv_commands.get_resolver()

rsv_project = resolver.get_rsv_project(project='cjd')

user = bsc_core.SystemMtd.get_user_name()
time_tag = bsc_core.SystemMtd.get_time_tag()

for i_asset in assets:
    i_rsv_task = rsv_project.get_rsv_task(asset=i_asset, task='surfacing')
    i_katana_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
    i_katana_scene_src_file_path = i_katana_scene_src_file_unit.get_result()
    if i_katana_scene_src_file_path:
        i_properties = i_katana_scene_src_file_unit.get_properties_by_result(i_katana_scene_src_file_path)
        i_version = i_properties.get('version')
        i_maya_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-maya-scene-src-file')
        i_maya_scene_src_file_path = i_maya_scene_src_file_unit.get_result(version=i_version)
        if utl_dcc_objects.OsFile(i_maya_scene_src_file_path).get_is_exists() is False:
            print 'CCCCCCCCC'
            # i_rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
            #     file_path=i_maya_scene_src_file_path
            # )
            #
            # i_export_query = ddl_objects.DdlRsvTaskQuery(
            #     'maya-scene-export', i_rsv_task_properties
            # )
            # i_export = ddl_methods.RsvTaskHookExecutor(
            #     method_option=i_export_query.get_method_option(),
            #     script_option=i_export_query.get_script_option(
            #         file=i_maya_scene_src_file_path,
            #         create_scene_src=True,
            #         with_scene=True,
            #         with_texture_tx=True,
            #         #
            #         user=user, time_tag=time_tag,
            #     )
            # )
            # i_export.set_run_with_deadline()


