# coding:utf-8
import sys

from lxmaya_fnc.scripts import _mya_fnc_scp_utility


def set_geometry_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_file_path = option_opt.get('file')
    scene_file_path = utl_core.Path.set_map_to_platform(scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'maya-geometry-export',
                'start'
            )
            #
            mya_scene_file_path = rsv_task_properties.get('any_scene_file')
            mya_dcc_objects.Scene.set_file_open(mya_scene_file_path)
            #
            _mya_fnc_scp_utility.set_export_check_run(
                rsv_task_properties
            )
            #
            with_geometry_usd = option_opt.get('with_geometry_usd') or False
            if with_geometry_usd is True:
                set_asset_geometry_usd_export(rsv_task_properties)
            #
            with_geometry_uv_map_usd = option_opt.get('with_geometry_uv_map_usd') or False
            if with_geometry_uv_map_usd is True:
                import lxusd_fnc.scripts as usd_scripts
                #
                usd_scripts.set_asset_geometry_uv_map_usd_export(rsv_task_properties)
            #
            with_geometry_uv_map_usd_link = option_opt.get('with_geometry_uv_map_usd_link') or False
            if with_geometry_uv_map_usd_link is True:
                import lxusd_fnc.scripts as usd_scripts
                #
                usd_scripts.set_asset_geometry_uv_map_usd_link_export(rsv_task_properties)
            #
            with_geometry_abc = option_opt.get('with_geometry_abc') or False
            if with_geometry_abc is True:
                pass
            #
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'maya-geometry-export',
                'complete'
            )
    else:
        utl_core.Log.set_module_warning_trace(
            key,
            u'file="{}" is not available'.format(scene_file_path)
        )


def set_asset_geometry_usd_export(rsv_task_properties):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxobj.objects as core_objects
    #
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    workspace = rsv_task_properties.get('workspace')
    version = rsv_task_properties.get('version')
    #
    root = rsv_task_properties.get('dcc.root')
    #
    asset_geometry_rsv_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
    #
    mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
        pathsep='|'
    )
    mya_root = mya_dcc_objects.Group(
        mya_root_dag_opt.get_value()
    )
    if mya_root.get_is_exists() is True:
        # location_names = [i.name for i in mya_root.get_children()]
        location_names = ['hi', 'shape', 'hair']
        with utl_core.GuiProgressesRunner.create(maximum=len(location_names), label='export geometry in location') as g_p:
            for i_location_name in location_names:
                g_p.set_update()
                #
                if workspace == 'work':
                    i_geometry_usd_var_file_path = asset_geometry_rsv_query.get_work_usd_var_file(
                        var=i_location_name, version=version
                    )
                elif workspace == 'publish':
                    i_geometry_usd_var_file_path = asset_geometry_rsv_query.get_usd_var_file_(
                        var_name=i_location_name, version=version
                    )
                else:
                    raise TypeError()
                #
                i_location = '{}/{}'.format(root, i_location_name)
                i_sub_root_dag_path = core_objects.ObjDagPath(i_location)
                i_mya_sub_root_dag_path = i_sub_root_dag_path.set_translate_to(
                    pathsep=ma_configure.Util.OBJ_PATHSEP
                )
                #
                sub_root_mya_obj = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
                if sub_root_mya_obj.get_is_exists() is True:
                    mya_fnc_exporters.GeometryUsdExporter_(
                        file_path=i_geometry_usd_var_file_path,
                        root=i_location,
                        option=dict(
                            default_prim_path=root,
                            with_uv=True,
                            with_mesh=True,
                            use_override=False
                        )
                    ).set_run()
                else:
                    utl_core.Log.set_module_warning_trace(
                        key,
                        'obj="{}" is non-exists'.format(i_location)
                    )


def set_asset_work_geometry_usd_export(rsv_task_properties):
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxobj.objects as core_objects
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    resolver = rsv_commands.get_resolver()
    rsv_task = resolver.get_rsv_task(**rsv_task_properties.value)
    #
    version = rsv_task_properties.get('version')
    #
    root = rsv_task_properties.get('dcc.root')
    #
    var_names = ['hi', 'lo', 'shape', 'temp']
    with utl_core.GuiProgressesRunner.create(maximum=len(var_names), label='export geometry in location') as g_p:
        for i_var_name in var_names:
            g_p.set_update()
            #
            i_sub_root = '{}/{}'.format(root, i_var_name)
            i_sub_root_dag_path = core_objects.ObjDagPath(i_sub_root)
            i_mya_sub_root_dag_path = i_sub_root_dag_path.set_translate_to(
                pathsep=ma_configure.Util.OBJ_PATHSEP
            )
            i_mya_sub_root = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
            if i_mya_sub_root.get_is_exists() is True:
                i_geometry_usd_file_unit = rsv_task.get_rsv_unit(keyword='asset-source-geometry-usd-var-file')
                i_geometry_usd_var_file_path = i_geometry_usd_file_unit.get_result(
                    version=version, extend_variants=dict(var=i_var_name)
                )
                mya_fnc_exporters.GeometryUsdExporter_(
                    file_path=i_geometry_usd_var_file_path,
                    root=i_sub_root,
                    option=dict(
                        default_prim_path=root,
                        with_uv=True,
                        with_mesh=True,
                        use_override=False
                    )
                ).set_run()


def set_geometry_import_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_file_path = option_opt.get('file')
    scene_file_path = utl_core.Path.set_map_to_platform(scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
    if rsv_task_properties:
        with_scene = option_opt.get('with_scene')
        if with_scene is True:
            mya_dcc_objects.Scene.set_file_open(scene_file_path)
        #
        with_geometry_uv_map = option_opt.get('with_geometry_uv_map') or False
        if with_geometry_uv_map is True:
            set_asset_geometry_uv_maps_import(rsv_task_properties)
        #
        if with_scene is True:
            version = rsv_task_properties.get('version')
            scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
                wokspace='publish', version=version
            )
            utl_dcc_objects.OsFile(scene_file_path).set_backup()
            mya_dcc_objects.Scene.set_file_save_to(scene_file_path)
    else:
        utl_core.Log.set_module_warning_trace(
            key,
            u'file="{}" is not available'.format(scene_file_path)
        )


def set_asset_geometry_uv_maps_import(rsv_task_properties):
    import lxmaya.fnc.builders as mya_fnc_builders
    #
    branch = rsv_task_properties.get('branch')
    step = rsv_task_properties.get('step')
    if branch == 'asset':
        if step in ['mod', 'srf']:
            project = rsv_task_properties.get('project')
            asset = rsv_task_properties.get('asset')
            #
            mya_fnc_builders.AssetBuilder(
                option=dict(
                    project=project,
                    asset=asset,
                    with_surface_geometry_uv_map=True,
                )
            ).set_run()
        #
        elif step in ['rig']:
            project = rsv_task_properties.get('project')
            asset = rsv_task_properties.get('asset')
            #
            mya_fnc_builders.AssetBuilder(
                option=dict(
                    project=project,
                    asset=asset,
                    with_surface_geometry_uv_map=True,
                    uv_map_face_vertices_contrast=True,
                )
            ).set_run()

