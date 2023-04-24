# coding:utf-8
from lxkatana_fnc.scripts import _ktn_fnc_scp_utility, _ktn_fnc_scp_texture


def set_look_export_by_any_scene_file(option):
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
    import lxshotgun_fnc.scripts as stg_fnc_scripts
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
        rsv_version.set('user', user)
        rsv_version.set('time_tag', time_tag)
        #
        force = option_opt.get('force') or False
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            utl_core.Log.set_module_result_trace(
                'katana-look-export',
                'option="{}"'.format(option)
            )
            scene_src_file_obj = utl_dcc_objects.OsFile(any_scene_file_path)
            if scene_src_file_obj.get_is_exists() is True:
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'katana-look-export',
                    'start'
                )
                #
                ktn_dcc_objects.Scene.set_file_open(any_scene_file_path)
                # texture
                with_texture = option_opt.get('with_texture') or False
                if with_texture is True:
                    _ktn_fnc_scp_texture.set_asset_texture_export(rsv_task_properties)
                else:
                    # texture-tx
                    with_texture_tx = option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        _ktn_fnc_scp_texture.set_asset_texture_tx_export(rsv_task_properties)
                #
                with_look_ass = option_opt.get('with_look_ass') or False
                if with_look_ass is True:
                    stg_fnc_scripts.set_version_log_module_result_trace(
                        rsv_task_properties,
                        'katana-look-ass-export',
                        'start'
                    )
                    set_asset_look_ass_export(rsv_task_properties, force)
                #
                with_look_klf = option_opt.get('with_look_klf') or False
                if with_look_klf is True:
                    stg_fnc_scripts.set_version_log_module_result_trace(
                        rsv_task_properties,
                        'katana-look-klf export',
                        'start'
                    )
                    set_asset_look_klf_export(rsv_task_properties, force)
                    set_asset_look_klf_extra_export(rsv_task_properties, force)
                #
                with_look_properties_usd = option_opt.get('with_look_properties_usd') or False
                if with_look_properties_usd is True:
                    set_asset_look_properties_usd_export(rsv_task_properties)
                #
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'katana-look-export',
                    'complete'
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'katana-look-export-script-run',
                    u'file="{}" is non-exists'.format(any_scene_file_path)
                )
    else:
        utl_core.Log.set_module_warning_trace(
            'katana-scene-look-export',
            u'file="{}" is not available'.format(any_scene_file_path)
        )


def set_asset_look_ass_export(rsv_task_properties, force=False):
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxkatana.fnc.exporters as ktn_fnc_exporters
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    version = rsv_task_properties.get('option.version')
    #
    ktn_workspace = ktn_dcc_objects.AssetWorkspace()
    #
    default_look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_file(
        version=version
    )
    default_look_ass_file = utl_dcc_objects.OsFile(default_look_ass_file_path)
    if default_look_ass_file.get_is_exists() is False or force is True:
        ktn_fnc_exporters.FncLookAssExporter(
            option=dict(
                file=default_look_ass_file_path,
                location='/master',
                look_pass_node=ktn_workspace.get_main_node('look_outputs'),
                look_pass='default'
            )
        ).set_run()
    else:
        utl_core.Log.set_module_warning_trace(
            'katana-look-ass-export',
            u'file="{}" is exists'.format(default_look_ass_file_path)
        )
    #
    look_pass_names = ktn_workspace.get_look_pass_names()
    #
    for i_look_pass_name in look_pass_names:
        if i_look_pass_name != 'default':
            i_look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_sub_file(
                look_pass=i_look_pass_name, version=version
            )
            #
            i_look_ass_file = utl_dcc_objects.OsFile(i_look_ass_file_path)
            if i_look_ass_file.get_is_exists() is False or force is True:
                i_look_pass_source_obj = ktn_workspace.get_pass_source_obj(i_look_pass_name)
                if i_look_pass_source_obj is not None:
                    ktn_fnc_exporters.FncLookAssExporter(
                        option=dict(
                            file=i_look_ass_file_path,
                            location='/master',
                            look_pass_node=ktn_workspace.get_main_node('look_outputs'),
                            look_pass=i_look_pass_name
                        )
                    ).set_run()


def set_asset_work_look_ass_export(rsv_task_properties, force=False):
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxkatana.fnc.exporters as ktn_fnc_exporters
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    version = rsv_task_properties.get('option.version')
    #
    default_look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_work_file(
        version=version
    )
    default_look_ass_file = utl_dcc_objects.OsFile(default_look_ass_file_path)
    ktn_workspace = ktn_dcc_objects.AssetWorkspace()
    if default_look_ass_file.get_is_exists() is False or force is True:
        ktn_fnc_exporters.FncLookAssExporter(
            option=dict(
                file=default_look_ass_file_path,
                location='/master',
                look_pass_node=ktn_workspace.get_main_node('look_outputs'),
                look_pass='default'
            )
        ).set_run()
    else:
        utl_core.Log.set_module_warning_trace(
            'katana-look-ass-export',
            u'file="{}" is exists'.format(default_look_ass_file_path)
        )


def set_asset_look_klf_export(rsv_task_properties, force=False):
    from lxutil import utl_core
    #
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    version = rsv_task_properties.get('option.version')
    #
    look_klf_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_klf_file(
        version=version
    )
    asset_workspace = ktn_dcc_objects.AssetWorkspace()
    #
    ktn_dcc_objects.Node('rootNode').get_port('variables.camera').set('asset_free')
    #
    asset_geometries_dcc_node = ktn_dcc_objects.Node('asset__geometries')
    if asset_geometries_dcc_node.get_is_exists() is True:
        asset_geometries_dcc_node.get_port('lynxi_variants.look').set('asset-work')
    else:
        raise RuntimeError(
            utl_core.Log.set_module_error_trace(
                'obj="{}" is non-exists'.format(
                    asset_geometries_dcc_node.path
                )
            )
        )
    #
    asset_workspace.set_look_klf_file_export(look_klf_file_path)


def set_asset_look_klf_extra_export(rsv_task_properties, force=False):
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.fnc.exporters as ktn_fnc_exporters
    #
    version = rsv_task_properties.get('option.version')
    #
    look_json_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_klf_extra_file(
        version=version
    )
    #
    ktn_fnc_exporters.LookKlfExtraExporter(
        file_path=look_json_file_path
    ).set_run()


def set_asset_look_properties_usd_export(rsv_task_properties):
    import lxutil_fnc.scripts as utl_fnc_scripts
    #
    utl_fnc_scripts.set_asset_look_properties_usd_export(
        rsv_task_properties
    )


def set_cfx_look_export_by_any_scene_file(option):
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
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.map_to_current(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    #
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        utl_core.Log.set_module_result_trace(
            'katana-look-export',
            'option="{}"'.format(option)
        )
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        version = rsv_task_properties.get('version')
        if branch == 'asset':
            create_scene_src = option_opt.get('create_scene_src') or False
            if create_scene_src is True:
                result = _ktn_fnc_scp_utility.set_asset_cfx_look_workspace_create(rsv_task_properties)
                if result is True:
                    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_katana_src_file(
                        version=version
                    )
                    ktn_dcc_objects.Scene.set_file_save_to(scene_src_file_path)
            #
            any_scene_file = utl_dcc_objects.OsFile(any_scene_file_path)
            if any_scene_file.get_is_exists() is True:
                ktn_dcc_objects.Scene.set_file_open(any_scene_file_path)
                #
                with_texture = option_opt.get('with_texture') or False
                if with_texture is True:
                    _ktn_fnc_scp_texture.set_asset_texture_export(
                        rsv_task_properties
                    )
                #
                with_scene = option_opt.get('with_scene') or False
                if with_scene is True:
                    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_katana_file(
                        version=version
                    )
                    ktn_dcc_objects.Scene.set_file_save_to(scene_file_path)
                # geometry uv-map
                rsv_asset_geometry_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
                surface_anm_geometry_uv_map_file_path = rsv_asset_geometry_query.get_usd_surface_anm_hi_file(version=version)
                surface_cfx_geometry_uv_map_file_path = rsv_asset_geometry_query.get_usd_surface_cfx_hi_file(version=version)
                utl_dcc_objects.OsFile(
                    surface_anm_geometry_uv_map_file_path
                ).set_copy_to_file(
                    surface_cfx_geometry_uv_map_file_path
                )
                #
                set_asset_look_ass_export(rsv_task_properties)
                set_asset_look_klf_export(rsv_task_properties)
                set_asset_look_klf_extra_export(rsv_task_properties)
                #
                import lxusd_fnc.scripts as usd_scripts
                #
                usd_scripts.set_asset_geometry_uv_map_usd_export(rsv_task_properties)
                #
                usd_scripts.set_asset_usd_set_export(rsv_task_properties)
