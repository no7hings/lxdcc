# coding:utf-8
from lxkatana_fnc.scripts import _ktn_fnc_scp_utility


def set_geometry_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.map_to_current(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        application = rsv_task_properties.get('application')
        rsv_version = resolver.get_rsv_task_version(**rsv_task_properties.value)
        if application != 'katana':
            any_scene_file_path = _ktn_fnc_scp_utility.get_asset_scene_src_file_path(rsv_version)
            rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            scene_src_file_obj = utl_dcc_objects.OsFile(any_scene_file_path)
            if scene_src_file_obj.get_is_exists() is True:
                ktn_dcc_objects.Scene.set_file_open(any_scene_file_path)
                # geometry
                with_geometry_usd = option_opt.get('with_geometry_usd') or False
                if with_geometry_usd is True:
                    set_asset_geometry_usd_export(rsv_task_properties)
                # geometry uv-map
                with_geometry_uv_map_usd = option_opt.get('with_geometry_uv_map_usd') or False
                if with_geometry_uv_map_usd is True:
                    import lxusd_fnc.scripts as usd_scripts
                    usd_scripts.set_asset_geometry_uv_map_usd_export(rsv_task_properties)
                # geometry uv-map
                with_geometry_uv_map_usd_link = option_opt.get('with_geometry_uv_map_usd_link') or False
                if with_geometry_uv_map_usd_link is True:
                    import lxusd_fnc.scripts as usd_scripts
                    usd_scripts.set_asset_geometry_uv_map_usd_link_export(rsv_task_properties)
            else:
                utl_core.Log.set_module_warning_trace(
                    'katana-geometry-export-script-run',
                    u'file="{}" is non-exists'.format(any_scene_file_path)
                )


def set_asset_geometry_usd_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    version = rsv_task_properties.get('option.version')
    workspace = 'publish'
    #
    asset_geometry_rsv_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
    geometry_surface_usd_file_path = asset_geometry_rsv_query.get_usd_surface_hi_file(
        workspace=workspace,
        version=version
    )
    #
    geometry_work_surface_usd_file_path = ktn_dcc_objects.AssetWorkspace().get_geometry_uv_map_usd_source_file()
    if geometry_work_surface_usd_file_path:
        stg_fnc_scripts.set_version_log_module_result_trace(
            rsv_task_properties,
            'katana-geometry-export',
            'start'
        )
        #
        utl_dcc_objects.OsFile(geometry_work_surface_usd_file_path).set_copy_to_file(
            geometry_surface_usd_file_path
        )
        #
        stg_fnc_scripts.set_version_log_module_result_trace(
            rsv_task_properties,
            'katana-geometry-export',
            'complete'
        )
