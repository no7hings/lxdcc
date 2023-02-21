# coding:utf-8


def set_usd_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_file_path = option_opt.get('file')
    scene_file_path = utl_core.Path.set_map_to_platform(scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
    if rsv_task_properties:
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'usd-export',
                'start'
            )
            #
            with_geometry_uv_map_usd = option_opt.get('with_geometry_uv_map_usd') or False
            if with_geometry_uv_map_usd is True:
                set_asset_geometry_uv_map_usd_export(rsv_task_properties)
            #
            with_usd_set = option_opt.get('with_usd_set') or False
            if with_usd_set is True:
                set_asset_usd_set_export(rsv_task_properties)
            #
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'usd-export',
                'complete'
            )
    else:
        utl_core.Log.set_module_warning_trace(
            'look-export',
            u'file="{}" is not available'.format(scene_file_path)
        )


def set_asset_geometry_uv_map_usd_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxusd.fnc.exporters as usd_fnc_exporters
    #
    version = rsv_task_properties.get('version')
    #
    root = rsv_task_properties.get('dcc.root')
    #
    asset_geometry_rsv_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
    # model geometry
    model_geometry_hi_usd_file_path = asset_geometry_rsv_query.get_usd_model_hi_file()
    # current geometry
    current_geometry_hi_usd_file_path = asset_geometry_rsv_query.get_usd_hi_file(
        version=version
    )
    # uv-map file
    geometry_usd_uv_map_file_path = asset_geometry_rsv_query.get_usd_uv_map_file(
        version=version
    )
    if geometry_usd_uv_map_file_path is not None:
        if model_geometry_hi_usd_file_path and current_geometry_hi_usd_file_path:
            usd_fnc_exporters.GeometryUvMapExporter(
                file_path=geometry_usd_uv_map_file_path,
                root=root,
                option=dict(
                    file_0=current_geometry_hi_usd_file_path,
                    file_1=current_geometry_hi_usd_file_path
                )
            ).set_run()


def set_asset_work_geometry_uv_map_usd_export(rsv_task_properties):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    import lxusd.fnc.exporters as usd_fnc_exporters
    #
    version = rsv_task_properties.get('version')
    #
    root = rsv_task_properties.get('dcc.root')
    #
    resolver = rsv_commands.get_resolver()
    rsv_task = resolver.get_rsv_task(**rsv_task_properties.value)
    #
    var_names = ['hi']
    #
    for i_var_name in var_names:
        i_geometry_usd_hi_file_unit = rsv_task.get_rsv_unit(keyword='asset-source-geometry-usd-var-file')
        i_geometry_usd_hi_file_path = i_geometry_usd_hi_file_unit.get_result(
            version=version, extend_variants=dict(var=i_var_name)
        )
        if i_geometry_usd_hi_file_path:
            i_geometry_usd_hi_file = utl_dcc_objects.OsFile(i_geometry_usd_hi_file_path)
            if i_geometry_usd_hi_file.get_is_exists() is True:
                i_geometry_uv_map_usd_file_unit = rsv_task.get_rsv_unit(keyword='asset-source-geometry-uv_map-usd-var-file')
                i_geometry_uv_map_usd_file_path = i_geometry_uv_map_usd_file_unit.get_result(
                    version=version, extend_variants=dict(var=i_var_name)
                )
                usd_fnc_exporters.GeometryUvMapExporter(
                    file_path=i_geometry_uv_map_usd_file_path,
                    root=root,
                    option=dict(
                        file_0=i_geometry_usd_hi_file_path,
                        file_1=i_geometry_usd_hi_file_path
                    )
                ).set_run()


def set_asset_geometry_uv_map_usd_link_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    asset_geometry_rsv_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
    # uv-map file
    surface_geometry_usd_uv_map_file_path = asset_geometry_rsv_query.get_usd_surface_uv_map_file()
    if surface_geometry_usd_uv_map_file_path:
        current_geometry_usd_uv_map_file_path = asset_geometry_rsv_query.get_usd_uv_map_file(
            version=version
        )
        utl_dcc_objects.OsFile(current_geometry_usd_uv_map_file_path).create_directory()
        utl_dcc_objects.OsFile(surface_geometry_usd_uv_map_file_path).set_link_to(
            current_geometry_usd_uv_map_file_path, replace=True
        )


def set_asset_usd_set_export(rsv_task_properties):
    import os
    #
    import fnmatch
    #
    from lxbasic import bsc_core
    #
    import lxutil.objects as utl_objects
    #
    import lxresolver.operators as rsv_operators
    #
    branch = rsv_task_properties.get('branch')
    if branch == 'asset':
        step = rsv_task_properties.get('step')
        if step in ['mod', 'srf']:
            task = rsv_task_properties.get('task')
            version = rsv_task_properties.get('version')
            #
            asset_look_rsv_query = rsv_operators.RsvAssetLookQuery(rsv_task_properties)
            asset_usd_rsv_query = rsv_operators.RsvAssetUsdQuery(rsv_task_properties)
            #
            look_klf_file_path = asset_look_rsv_query.get_klf_file(
                version=version
            )
            # usd-geometry-uv-map
            geometry_usd_uv_map_file_path = asset_usd_rsv_query.get_geometry_uv_map_look_file(
                version=version
            )
            # usd-look
            look_usd_file_path = asset_usd_rsv_query.get_look_file(
                version=version
            )
            look_properties_file_dict = asset_usd_rsv_query.get_look_properties_file_dict(
                version=version
            )
            element_names = bsc_core.StgZipFileOpt(look_klf_file_path).get_element_names()
            look_pass_names = [os.path.splitext(i)[0] for i in fnmatch.filter(element_names, '*.klf')]
            if look_pass_names:
                utl_objects.DotUsdaFile(
                    file_path=look_usd_file_path
                ).set_surface_look_write(
                    look_root_name='look',
                    look_pass_name=look_pass_names[0],
                    look_pass_names=look_pass_names,
                    look_file_path=look_klf_file_path,
                    look_properties_file_dict=look_properties_file_dict
                )
            #
            usd_registry_file_path = asset_usd_rsv_query.get_registry_file(
                version=version
            )
            utl_objects.DotUsdaFile(
                file_path=usd_registry_file_path
            ).set_surface_registry_write(
                look_file_path=look_usd_file_path,
                uv_map_file_path=geometry_usd_uv_map_file_path,
            )
            #
            if task in ['modeling', 'surfacing', 'srf_anishading', 'srf_cfxshading']:
                # noinspection PyUnresolvedReferences
                import production.gen.record_set_registry as pgs
                pgs.run(usd_registry_file_path)


def set_usd_create_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_file_path = option_opt.get('file')
    scene_file_path = utl_core.Path.set_map_to_platform(scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
    if rsv_task_properties:
        rsv_version = resolver.get_rsv_task_version(**rsv_task_properties.value)
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_version.set('user', user)
        rsv_version.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'usd create',
                'start'
            )
            #
            with_component_usd = option_opt.get('with_component_usd') or False
            if with_component_usd is True:
                create_set_asset_component_usd(rsv_version)
            #
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'usd create',
                'complete'
            )
    else:
        utl_core.Log.set_module_warning_trace(
            'usd create',
            u'file="{}" is not available'.format(scene_file_path)
        )


def create_set_asset_component_usd(rsv_version):
    from lxutil import utl_configure
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    step = rsv_version.get('step')
    #
    usd_directory_unit = rsv_version.get_rsv_unit(
        keyword='asset-component-usd-dir'
    )
    #
    usd_directory_path = usd_directory_unit.get_result(version=rsv_version.get('version'))
    #
    key_map_dict = dict(
        mod='usda/set/model',
        srf='usda/set/surface'
    )
    if step in key_map_dict:
        key = key_map_dict[step]
        #
        c = utl_configure.Jinja.get_configure(key)
        c.set_update(
            rsv_version.properties.value
        )
        #
        c.set_flatten()
        #
        usda_dict = c.get('usdas')
        #
        for k, v in usda_dict.items():
            t = utl_configure.Jinja.get_template('{}/{}'.format(key, k))
            i_raw = t.render(
                **c.value
            )
            i_usda_file_path = '{}/{}'.format(
                usd_directory_path, v
            )
            #
            utl_dcc_objects.OsFile(i_usda_file_path).set_write(
                i_raw
            )

