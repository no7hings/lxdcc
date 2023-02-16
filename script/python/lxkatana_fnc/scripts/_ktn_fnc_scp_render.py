# coding:utf-8
from lxkatana_fnc.scripts import _ktn_fnc_scp_utility


def set_render_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    from lxdeadline import ddl_core
    #
    import lxdeadline.objects as ddl_objects
    #
    import lxdeadline.methods as ddl_methods
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    td_enable = option_opt.get('td_enable') or False
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        #
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            # create camera for render
            create_camera = option_opt.get('create_camera') or False
            if create_camera is True:
                maya_camera_export_query = ddl_objects.DdlRsvTaskQuery(
                    'maya-camera-export', rsv_task_properties
                )
                maya_camera_export = ddl_methods.RsvTaskHookExecutor(
                    method_option=maya_camera_export_query.get_method_option(),
                    script_option=maya_camera_export_query.get_script_option(
                        file=any_scene_file_path,
                        with_camera_persp_abc=True,
                        #
                        td_enable=td_enable,
                        #
                        user=user, time_tag=time_tag
                    )
                )
                maya_camera_export.execute_with_deadline()
            #
            create_scene = option_opt.get('create_scene') or False
            if create_scene is True:
                katana_render_scene_create_query = ddl_objects.DdlRsvTaskQuery(
                    'katana-render-scene-create', rsv_task_properties
                )
                katana_render_scene_create = ddl_methods.RsvTaskHookExecutor(
                    method_option=katana_render_scene_create_query.get_method_option(),
                    script_option=katana_render_scene_create_query.get_script_option(
                        file=any_scene_file_path,
                        #
                        td_enable=td_enable,
                        #
                        user=user, time_tag=time_tag
                    ),
                    job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                        [
                            # maya-camera-create
                            ddl_objects.DdlRsvTaskQuery(
                                'maya-camera-export', rsv_task_properties
                            ).get_method_option(),
                        ]
                    )
                )
                katana_render_scene_create.execute_with_deadline()
            #
            create_render = option_opt.get('create_render') or False
            if create_render is True:
                with_shotgun_render = option_opt.get('with_shotgun_render') or False
                #
                width = option_opt.get('width') or 512
                height = option_opt.get('height') or 512
                #
                katana_render_create_query = ddl_objects.DdlRsvTaskQuery(
                    'katana-render-create', rsv_task_properties
                )
                katana_render_create = ddl_methods.RsvTaskHookExecutor(
                    method_option=katana_render_create_query.get_method_option(),
                    script_option=katana_render_create_query.get_script_option(
                        file=any_scene_file_path,
                        with_shotgun_render=with_shotgun_render,
                        width=width, height=height,
                        #
                        td_enable=td_enable,
                        #
                        user=user, time_tag=time_tag
                    ),
                    job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                        [
                            # maya-camera-create
                            ddl_objects.DdlRsvTaskQuery(
                                'maya-camera-export', rsv_task_properties
                            ).get_method_option(),
                            # katana-render-scene-create
                            ddl_objects.DdlRsvTaskQuery(
                                'katana-render-scene-create', rsv_task_properties
                            ).get_method_option(),
                        ]
                    )
                )
                katana_render_create.execute_with_deadline()


# render scene export
def set_render_scene_create_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
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
        #
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            set_asset_render_scene_create(rsv_task_properties)


def set_asset_render_scene_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxkatana.fnc.builders as ktn_fnc_builders
    #
    import lxkatana.fnc.importers as ktn_fnc_importers
    #
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    step = rsv_task_properties.get('step')
    task = rsv_task_properties.get('task')
    version = rsv_task_properties.get('version')
    #
    result = _ktn_fnc_scp_utility.set_asset_workspace_create(
        rsv_task_properties,
        use_preview_look_pass=False
    )
    if result is True:
        ktn_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                #
                with_camera=True,
                camera_option='step={}&task={}&version={}'.format(
                    step,
                    task,
                    version
                )
            )
        ).set_run()
        #
        render_katana_scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_render_katana_scene_file(
            version=version
        )
        ktn_dcc_objects.Scene.set_file_save_to(render_katana_scene_file_path)
        ktn_fnc_importers.LookAssImporter._set_pst_run_()
        #
        render_output_directory_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_render_output_dir(
            version=version
        )
        utl_dcc_objects.OsDirectory_(render_output_directory_path).set_create()
        #
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        look_pass_names = ktn_workspace.get_look_pass_names()
        for i_look_pass_name in look_pass_names:
            node = ktn_dcc_objects.Node('{}__render_outputs'.format(i_look_pass_name))
            if node.get_is_exists() is True:
                node.get_port('outputPath').set(
                    render_output_directory_path
                )
        #
        n = ktn_dcc_objects.Node('render_settings')
        if n.get_is_exists() is True:
            n.get_port('arnold_render_settings.stats_file_enable').set(1)
            n.get_port('arnold_render_settings.stats_file').set(
                '{}/<camera>/<look-pass>.stats.####.json'.format(render_output_directory_path)
            )
            #
            n.get_port('arnold_render_settings.profile_file_enable').set(1)
            n.get_port('arnold_render_settings.profile_file').set(
                '{}/<camera>/<look-pass>.profile.####.json'.format(render_output_directory_path)
            )
            n.get_port('lynxi_settings.render_output_enable').set(1)
            n.get_port('lynxi_settings.render_output').set(
                '{}/<camera>/<look-pass>/<render-pass>.####.exr'.format(render_output_directory_path)
            )
        #
        n = ktn_dcc_objects.Node('light_rigs')
        if n.get_is_exists() is True:
            n.get_port('user.render_quality').set(1)
        #
        ktn_dcc_objects.Scene.set_file_save_to(
            render_katana_scene_file_path
        )


def set_render_create_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxkatana.fnc.builders as ktn_fnc_builders
    #
    import lxdeadline.objects as ddl_objects
    #
    from lxdeadline import ddl_core
    #
    import lxdeadline.methods as ddl_methods
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    td_enable = option_opt.get('td_enable') or False
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
            version = rsv_task_properties.get('version')
            #
            render_katana_file_path = rsv_operators.RsvAssetSceneQuery(
                rsv_task_properties).get_render_katana_scene_file(
                version=version
            )
            #
            ktn_dcc_objects.Scene.set_file_open(render_katana_file_path)
            ktn_workspace = ktn_dcc_objects.AssetWorkspace()
            width = option_opt.get('width') or 512
            height = option_opt.get('height') or 512
            ktn_workspace.set_render_resolution(width, height)
            ktn_dcc_objects.Scene.set_file_save()
            # katana render
            look_pass_names = ktn_workspace.get_look_pass_names()
            for i_look_pass_name in look_pass_names:
                i_katana_scene_render_query = ddl_objects.DdlRsvTaskQuery(
                    'katana-render', rsv_task_properties
                )
                i_katana_scene_render = ddl_methods.DdlRsvTaskRender(
                    method_option=i_katana_scene_render_query.get_method_option(),
                    script_option=i_katana_scene_render_query.get_script_option(
                        file=any_scene_file_path,
                        render_file=render_katana_file_path,
                        width=width, height=height,
                        quality='R2',
                        frame=1,
                        renderer='{}__renderer'.format(i_look_pass_name),
                        #
                        td_enable=td_enable,
                        #
                        user=user, time_tag=time_tag,
                    )
                )
                i_katana_scene_render.execute_with_deadline()
            # shotgun render
            with_shotgun_render = option_opt.get('with_shotgun_render') or False
            if with_shotgun_render is True:
                shotgun_render_export_query = ddl_objects.DdlRsvTaskQuery(
                    'shotgun-render-export', rsv_task_properties
                )
                shotgun_render_export = ddl_methods.RsvTaskHookExecutor(
                    method_option=shotgun_render_export_query.get_method_option(),
                    script_option=shotgun_render_export_query.get_script_option(
                        file=any_scene_file_path,
                        with_asset_info=True,
                        with_look_pass_info=True,
                        #
                        td_enable=td_enable,
                        #
                        user=user, time_tag=time_tag
                    ),
                    job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                        [
                            # katana-render
                            ddl_objects.DdlRsvTaskQuery(
                                'katana-render', rsv_task_properties
                            ).get_method_option(),
                        ]
                    )
                )
                shotgun_render_export.execute_with_deadline()
