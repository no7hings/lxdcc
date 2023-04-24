# coding:utf-8


def set_shotgun_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_src_file_path = option_opt.get('file')
    scene_src_file_path = utl_core.Path.map_to_current(scene_src_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)
    if rsv_task_properties:
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
            time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
            rsv_task_properties.set('user', user)
            rsv_task_properties.set('time_tag', time_tag)
            #
            set_version_log_module_result_trace(
                rsv_task_properties,
                'shotgun-export',
                'start'
            )
            #
            with_shotgun_version = option_opt.get('with_shotgun_version') or False
            if with_shotgun_version is True:
                set_version_update(rsv_task_properties)
            #
            with_link = option_opt.get('with_link') or False
            if with_link is True:
                set_link_export(rsv_task_properties)
            #
            with_shotgun_dependency = option_opt.get('with_shotgun_dependency') or False
            if with_shotgun_dependency is True:
                set_dependents_export(rsv_task_properties)
            #
            set_version_log_module_result_trace(
                rsv_task_properties,
                'shotgun-export',
                'complete'
            )


def set_version_update(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxshotgun.objects as stg_objects
    #
    import lxshotgun.operators as stg_operators
    #
    stg_connector = stg_objects.StgConnector()
    #
    stg_task_query = stg_connector.get_stg_task_query(
        **rsv_task_properties.value
    )
    stg_version_query = stg_connector.get_stg_version_query(
        **rsv_task_properties.value
    )
    if stg_version_query is None:
        stg_connector.set_stg_version_create(
            **rsv_task_properties.value
        )
        stg_version_query = stg_connector.get_stg_version_query(
            **rsv_task_properties.value
        )
    #
    stg_task_opt = stg_operators.StgTaskOpt(stg_task_query)
    stg_task_opt.set_stg_last_version(stg_version_query.stg_obj)
    #
    stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)
    #
    stg_tag = stg_connector.get_stg_tag_force('td-batch')
    stg_version_opt.set_stg_tags_append(
        stg_tag
    )
    stg_version_type_ = rsv_task_properties.get('shotgun.stg_version_type')
    if stg_version_type_ is not None:
        stg_version_type = stg_version_type_
        stg_version_opt.set_stg_type(stg_version_type)
    #
    stg_status_ = rsv_task_properties.get('shotgun.stg_status')
    if stg_status_ is not None:
        stg_status = stg_status_
        stg_version_opt.set_stg_status(stg_status)
    #
    stg_todo_ = rsv_task_properties.get('shotgun.stg_todo')
    if stg_todo_ is not None:
        stg_todo = stg_todo_
        stg_version_opt.set_stg_todo(stg_todo)
    #
    description_ = rsv_task_properties.get('shotgun.description')
    if description_ is not None:
        description = description_
        stg_version_opt.set_description(description)
    #
    workspace = 'publish'
    version = rsv_task_properties.get('version')
    #
    movie = stg_version_opt.get_movie()
    if not movie:
        asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
        #
        preview_mov_file_path = asset_scene_query.get_preview_mov_file(
            workspace=workspace,
            version=version
        )
        stg_version_opt.set_movie_upload(preview_mov_file_path)
        #
        review_mov_file_path = asset_scene_query.get_review_mov_file(
            workspace=workspace,
            version=version
        )
        stg_version_opt.set_movie_upload(review_mov_file_path)


def set_version_log_module_result_trace(rsv_task_properties, module, result):
    pass
    # from lxutil import utl_core
    # #
    # import lxshotgun.objects as stg_objects
    # #
    # import lxresolver.operators as rsv_operators
    # #
    # import lxshotgun.operators as stg_operators
    # #
    # stg_connector = stg_objects.StgConnector()
    # #
    # stg_version_query = stg_connector.get_stg_version_query(
    #     **rsv_task_properties.value
    # )
    # if stg_version_query is None:
    #     stg_connector.set_stg_version_create(
    #         **rsv_task_properties.value
    #     )
    #     stg_version_query = stg_connector.get_stg_version_query(
    #         **rsv_task_properties.value
    #     )
    #     stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)
    #     workspace = 'publish'
    #     version = rsv_task_properties.get('version')
    #     task_version_directory_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_task_version_directory(
    #         workspace=workspace,
    #         version=version
    #     )
    #     stg_version_opt.set_folder(task_version_directory_path)
    # #
    # stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)
    # #
    # stg_version_opt.set_log_add(
    #     utl_core.Log.set_module_result_trace(
    #         module,
    #         result
    #     )
    # )


def set_link_export(rsv_task_properties):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    workspace = rsv_task_properties.get('workspace')
    version = rsv_task_properties.get('version')
    #
    task_version_directory_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_task_version_directory(
        workspace=workspace,
        version=version
    )

    task_no_version_directory_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_task_no_version_directory(
        workspace=workspace,
        version=version
    )

    utl_dcc_objects.OsDirectory_(task_version_directory_path).set_link_to(
        task_no_version_directory_path, replace=True
    )


def set_dependents_export(rsv_task_properties):
    import lxshotgun.objects as stg_objects
    #
    import lxresolver.commands as rsv_commands
    #
    import lxshotgun.operators as stg_operators
    #
    stg_connector = stg_objects.StgConnector()
    #
    stg_version_query = stg_connector.get_stg_version_query(
        **rsv_task_properties.value
    )
    #
    stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)

    resolver = rsv_commands.get_resolver()
    #
    project = rsv_task_properties.get('project')
    branch = rsv_task_properties.get('branch')
    if branch == 'asset':
        asset = rsv_task_properties.get('asset')
        rsv_model_task = resolver.get_rsv_task(
            project=project,
            asset=asset,
            step='mod',
            task='modeling'
        )
        model_geometry_usd_hi_file = rsv_model_task.get_rsv_unit(
            keyword='asset-geometry-usd-hi-file'
        )
        model_geometry_usd_hi_file_path = model_geometry_usd_hi_file.get_result(version='latest')
        if model_geometry_usd_hi_file_path:
            rsv_unit_properties = model_geometry_usd_hi_file.get_properties_by_result(model_geometry_usd_hi_file_path)
            stg_model_version = stg_connector.get_stg_version(**rsv_unit_properties.value)
            stg_version_opt.set_link_model_version(
                stg_model_version
            )


def set_render_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_src_file_path = option_opt.get('file')
    scene_src_file_path = utl_core.Path.map_to_current(scene_src_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)
    if rsv_task_properties:
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
            time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
            rsv_task_properties.set('user', user)
            rsv_task_properties.set('time_tag', time_tag)
            #
            with_look_pass_info = option_opt.get('with_look_pass_info') or False
            if with_look_pass_info is True:
                set_asset_look_pass_update(rsv_task_properties)
            #
            with_asset_info = option_opt.get('with_asset_info') or False
            if with_asset_info is True:
                set_asset_render_info_update(rsv_task_properties)


def set_asset_look_pass_update(rsv_task_properties):
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxshotgun.objects as stg_objects
    #
    import lxshotgun.operators as stg_operators
    #
    import lxarnold.operators as and_operators
    #
    resolver = rsv_commands.get_resolver()
    #
    force = False
    #
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    version = rsv_task_properties.get('version')
    #
    stg_connector = stg_objects.StgConnector()
    #
    stg_project_query = stg_connector.get_stg_project_query(
        **rsv_task_properties.value
    )
    stg_surface_version = stg_connector.get_stg_version(
        **rsv_task_properties.value
    )
    #
    color_space = stg_project_query.get('sg_colorspace')
    #
    rsv_task = resolver.get_rsv_task(
        **rsv_task_properties.value
    )
    render_output_sub_directory_unit = rsv_task.get_rsv_unit(keyword='asset-render-output-sub-dir')
    render_output_sub_directory_paths = render_output_sub_directory_unit.get_results(
        version=version, check_exists=True
    )
    for i_render_output_sub_directory_path in render_output_sub_directory_paths:
        i_properties = render_output_sub_directory_unit.get_properties_by_result(
            i_render_output_sub_directory_path
        )
        i_beauty_image_file_path = '{}/beauty.####.exr'.format(i_render_output_sub_directory_path)
        i_beauty_image_file = utl_dcc_objects.OsFile(i_beauty_image_file_path)
        if i_beauty_image_file.get_is_exists():
            i_look_pass_name = i_properties.get('look_pass')
            i_render_mov_sub_file_unit = rsv_task.get_rsv_unit(keyword='asset-render-mov-sub-file')
            i_render_mov_sub_file_path = i_render_mov_sub_file_unit.get_result(
                version=version, extend_variants=dict(
                    look_pass=i_look_pass_name
                )
            )
            stg_operators.ImgFileOpt(
                i_beauty_image_file
            ).set_convert_to(
                i_render_mov_sub_file_path, color_space=color_space
            )
            #
            i_render_jpg_sub_file_unit = rsv_task.get_rsv_unit(keyword='asset-render-jpg-sub-file')
            i_render_jpg_sub_file_path = i_render_jpg_sub_file_unit.get_result(
                version=version, extend_variants=dict(
                    look_pass=i_look_pass_name
                )
            )
            stg_operators.ImgFileOpt(
                i_beauty_image_file
            ).set_convert_to(
                i_render_jpg_sub_file_path, color_space=color_space
            )
            #
            i_look_pass_code = '{}.{}'.format(asset, i_look_pass_name)
            #
            stg_look_pass = stg_connector.get_stg_look_pass(
                project=project,
                asset=asset,
                look_pass_code=i_look_pass_code
            )
            if stg_look_pass is None:
                stg_connector.set_stg_look_pass_create(
                    project=project,
                    asset=asset,
                    look_pass_code=i_look_pass_code
                )
            #
            i_stg_look_pass_query = stg_connector.get_stg_look_pass_query(
                project=project,
                asset=asset,
                look_pass_code=i_look_pass_code
            )
            #
            i_stg_look_pass_opt = stg_operators.StgLookPassOpt(i_stg_look_pass_query)
            i_stg_look_pass_opt.set_image_upload(i_render_jpg_sub_file_path)
            if stg_surface_version is not None:
                i_stg_look_pass_opt.set_link_surface_version(stg_surface_version)
            #
            i_stats_file_path = '{}.stats.####.json'.format(i_render_output_sub_directory_path)
            i_stats_file = utl_dcc_objects.OsFile(i_stats_file_path)
            if i_stats_file.get_is_exists() is True:
                i_stg_look_pass_opt.set_link_render_stats_file(
                    i_stats_file.get_exists_file_paths()[0]
                )
            #
            i_profile_file_path = '{}.profile.####.json'.format(i_render_output_sub_directory_path)
            i_profile_file = utl_dcc_objects.OsFile(i_profile_file_path)
            if i_profile_file.get_is_exists() is True:
                i_stg_look_pass_opt.set_link_render_profile_file(
                    i_profile_file.get_exists_file_paths()[0]
                )
            #
            i_stats_file_opt = and_operators.StatsFileOpt(
                utl_dcc_objects.OsFile(
                    i_stats_file.get_exists_file_paths()[0]
                )
            )
            #
            i_warnings = i_stats_file_opt.get_warnings()
            i_stg_look_pass_query.set(
                'sg_render_warnings', u'\n'.join(i_warnings)
            )


def set_asset_render_info_update(rsv_task_properties):
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxshotgun.objects as stg_objects
    #
    import lxarnold.operators as and_operators
    #
    from lxbasic import bsc_core
    #
    import lxshotgun.operators as stg_operators
    #
    resolver = rsv_commands.get_resolver()
    #
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    version = rsv_task_properties.get('version')
    #
    stg_connector = stg_objects.StgConnector()
    #
    stg_asset_query = stg_connector.get_stg_resource_query(
        **rsv_task_properties.value
    )
    #
    rsv_task = resolver.get_rsv_task(
        **rsv_task_properties.value
    )
    render_output_sub_directory_unit = rsv_task.get_rsv_unit(
        keyword='asset-render-output-sub-dir',
    )
    #
    render_output_sub_directory_path = render_output_sub_directory_unit.get_result(
        version=version, extend_variants=dict(look_pass='default')
    )
    #
    if render_output_sub_directory_path:
        stats_file_path = '{}.stats.####.json'.format(render_output_sub_directory_path)
        stats_file = utl_dcc_objects.OsFile(stats_file_path)
        if stats_file.get_is_exists() is True:
            stats_file_opt = and_operators.StatsFileOpt(
                utl_dcc_objects.OsFile(
                    stats_file.get_exists_file_paths()[0]
                )
            )
            #
            peak_memory_gb = stats_file_opt.get_peak_memory_gb()
            if peak_memory_gb is not None:
                stg_asset_query.set(
                    'sg_render_memory', peak_memory_gb
                )
            #
            startup_memory_gb = stats_file_opt.get_startup_memory_gb()
            if startup_memory_gb is not None:
                stg_asset_query.set(
                    'sg_startup_render_memory', startup_memory_gb
                )
            #
            geometry_memory_gb = stats_file_opt.get_geometry_memory_gb()
            if geometry_memory_gb is not None:
                stg_asset_query.set(
                    'sg_geometry_render_memory', geometry_memory_gb
                )
            #
            mesh_memory_gb = stats_file_opt.get_mesh_memory_gb()
            if mesh_memory_gb is not None:
                stg_asset_query.set(
                    'sg_mesh_render_memory', mesh_memory_gb
                )
            #
            curve_memory_gb = stats_file_opt.get_curve_memory_gb()
            if curve_memory_gb is not None:
                stg_asset_query.set(
                    'sg_curve_render_memory', curve_memory_gb
                )
            #
            texture_memory_gb = stats_file_opt.get_texture_memory_gb()
            if texture_memory_gb is not None:
                stg_asset_query.set(
                    'sg_texture_render_memory', texture_memory_gb
                )
            #
            geometry_mesh_face_count = stats_file_opt.get_geometry_mesh_face_count()
            if geometry_mesh_face_count is not None:
                stg_asset_query.set(
                    'sg_subd_face_count', geometry_mesh_face_count
                )
            #
            hours = stats_file_opt.get_hours()
            if hours is not None:
                stg_asset_query.set(
                    'sg_render_time', hours
                )
            #
            startup_hours = stats_file_opt.get_startup_hours()
            if startup_hours is not None:
                stg_asset_query.set(
                    'sg_startup_render_time', startup_hours
                )
            #
            mesh_max_subdiv_iteration = stats_file_opt.get_mesh_max_subdiv_iteration()
            if mesh_max_subdiv_iteration is not None:
                stg_asset_query.set(
                    'sg_max_subd', mesh_max_subdiv_iteration
                )


def set_shotgun_create_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.map_to_current(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        rsv_version = resolver.get_rsv_task_version(**rsv_task_properties.value)
        #
        user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
        time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
        rsv_version.set('user', user)
        rsv_version.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            create_shotgun_task = option_opt.get('create_shotgun_version') or False
            if create_shotgun_task is True:
                set_asset_shotgun_task_create(rsv_version)
            #
            create_shotgun_version = option_opt.get('create_shotgun_version') or False
            if create_shotgun_version is True:
                set_asset_shot_version_create(rsv_version)
    else:
        utl_core.Log.set_module_warning_trace(
            'shotgun-version create',
            u'file="{}" is not available'.format(any_scene_file_path)
        )


def set_asset_shotgun_task_create(rsv_version):
    from lxutil import utl_core
    #
    import lxshotgun.objects as stg_objects
    #
    kwargs = rsv_version.properties.value
    #
    stg_connector = stg_objects.StgConnector()
    #
    stg_project = stg_connector.get_stg_project(
        **kwargs
    )
    if stg_project is not None:
        stg_entity = stg_connector.get_stg_resource(
            **kwargs
        )
        if stg_entity is None:
            stg_connector.create_stg_resource(**kwargs)
        #
        stg_step = stg_connector.get_stg_step(
            **kwargs
        )
        if stg_step is not None:
            stg_task = stg_connector.get_stg_task(
                **kwargs
            )
            if stg_task is None:
                stg_connector.set_stg_task_create(
                    **kwargs
                )
        else:
            utl_core.Log.set_module_error_trace(
                'shotgun-entity create',
                'step="{}" is non-exists.'.format(kwargs['step'])
            )
    else:
        utl_core.Log.set_module_error_trace(
            'shotgun-entity create',
            'project="{}" is non-exists.'.format(kwargs['project'])
        )


def set_asset_shot_version_create(rsv_version):
    from lxutil import utl_core
    #
    import lxshotgun.objects as stg_objects
    #
    kwargs = rsv_version.properties.value
    #
    stg_connector = stg_objects.StgConnector()
    #
    stg_task = stg_connector.get_stg_task(
        **kwargs
    )
    if stg_task is not None:
        stg_connector.set_stg_version_create(
            **kwargs
        )
    else:
        utl_core.Log.set_module_error_trace(
            'shotgun-entity create',
            'task="{}" is non-exists.'.format(kwargs['task'])
        )
