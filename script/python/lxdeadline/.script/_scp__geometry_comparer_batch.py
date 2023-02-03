# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxresolver.commands as rsv_commands

from lxutil import utl_configure

import lxusd.fnc.comparers as usd_fnc_comparers

assets = [
    # 'shrubs_a',
    # 'shrubs_b',
    # 'shrubs_c',
    # 'chrysanthemum_a',
    # 'chrysanthemum_b',
    # 'chrysanthemum_c',
    # 'kite_tree',
    # 'xiangzhang_tree_b',
    # 'xiangzhang_tree_b',
    # 'xiangzhang_tree_c',
    # 'xiangzhang_tree_d',
    # 'xiangzhang_tree_e',
    # 'xiangzhang_tree_f',
    'xiangzhang_tree_g'
]

resolver = rsv_commands.get_resolver()

rsv_project = resolver.get_rsv_project(project='cgm')

user = bsc_core.SystemMtd.get_user_name()
time_tag = bsc_core.SystemMtd.get_time_tag()

keyword = 'asset-geometry-usd-var-file'


list_ = []
for i_asset in assets:
    i_model_static_rsv_task = rsv_project.get_rsv_task(
        asset=i_asset, task='modeling'
    )
    i_model_dynamic_rsv_task = rsv_project.get_rsv_task(
        asset=i_asset, task='mod_dynamic'
    )

    i_surface_rsv_task = rsv_project.get_rsv_task(
        asset=i_asset, task='surfacing'
    )

    if i_model_static_rsv_task and i_model_dynamic_rsv_task:
        i_model_static_file_rsv_unit = i_model_static_rsv_task.get_rsv_unit(keyword=keyword)
        i_model_static_file_path = i_model_static_file_rsv_unit.get_result(version='latest', extend_variants=dict(var='hi'))
        i_dynamic_file_rsv_unit = i_model_dynamic_rsv_task.get_rsv_unit(keyword=keyword)
        i_dynamic_file_path = i_dynamic_file_rsv_unit.get_result(version='latest', extend_variants=dict(var='hi'))
        if i_model_static_file_path and i_dynamic_file_path:
            i_results = usd_fnc_comparers.GeometryComparer(
                option=dict(
                    file_src=i_model_static_file_path,
                    file_tgt=i_dynamic_file_path,
                    #
                    location='/master/hi'
                )
            ).get_results(
                check_status_includes=[
                    utl_configure.DccMeshCheckStatus.ADDITION,
                    utl_configure.DccMeshCheckStatus.DELETION,
                    #
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
                    #
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
            )
            if i_results:
                print i_results
                print i_model_static_file_path, i_dynamic_file_path
                list_.append(i_asset)
                utl_core.Log.set_error_trace(
                    'asset="{}" is non matched'.format(i_asset)
                )
        else:
            utl_core.Log.set_warning_trace(
                'asset="{}" is non data'.format(i_asset)
            )

print list_
