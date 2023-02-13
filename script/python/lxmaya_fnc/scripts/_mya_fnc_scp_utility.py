# coding:utf-8
import sys


def get_asset_scene_src_file_path(rsv_version):
    return rsv_version.get_rsv_unit(
        keyword='asset-maya-scene-src-file'
    ).get_result(version=rsv_version.get('version'))


def set_asset_workspace_create(rsv_task_properties):
    import lxmaya.fnc.builders as mya_fnc_builders
    #
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    #
    mya_fnc_builders.AssetBuilder(
        option=dict(
            project=project,
            asset=asset,
            #
            with_model_geometry=True,
            with_model_act_geometry_dyn=True,
            with_model_act_geometry_dyn_connect=True,
            #
            with_surface_look=True,
            with_surface_geometry_uv_map=True,
            #
            model_act_properties=['pg_start_frame', 'pg_end_frame'],
            geometry_var_names=['hi'],
        )
    ).set_run()


def set_asset_cfx_workspace_create(rsv_task_properties):
    import lxmaya.fnc.builders as mya_fnc_builders
    #
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    #
    mya_fnc_builders.AssetBuilder(
        option=dict(
            project=project,
            asset=asset,
            #
            with_surface_cfx_geometry=True,
            #
            with_surface_cfx_look=True,
            #
            geometry_var_names=['hi'],
        )
    ).set_run()
    return True


def set_asset_look_preview_workspace_pre_create(rsv_task_properties):
    import lxmaya.fnc.builders as mya_fnc_builders
    #
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    #
    mya_fnc_builders.AssetBuilder(
        option=dict(
            project=project,
            asset=asset,
            #
            with_model_geometry=True,
            #
            with_surface_look=True,
            with_surface_geometry_uv_map=True,
            #
            geometry_var_names=['hi'],
        )
    ).set_run()


def set_export_check_run(rsv_task_properties):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    dcc_pathsep = rsv_task_properties.get('dcc.pathsep')
    dcc_root = rsv_task_properties.get('dcc.root')
    #
    dcc_root_dag_opt = bsc_core.DccPathDagOpt(dcc_root)
    mya_root_dag_opt = dcc_root_dag_opt.set_translate_to(
        pathsep=dcc_pathsep
    )
    #
    if mya_dcc_objects.Group(mya_root_dag_opt.value).get_is_exists() is False:
        raise RuntimeError(
            utl_core.Log.set_module_error_trace(
                key,
                'obj="{}" is non-exists'.format(mya_root_dag_opt.value)
            )
        )


def set_work_file_link_to_temporary(rsv_task_properties, keyword):
    pass
