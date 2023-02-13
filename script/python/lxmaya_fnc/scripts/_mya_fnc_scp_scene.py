# coding:utf-8
from lxmaya_fnc.scripts import _mya_fnc_scp_utility, _mya_fnc_scp_texture


# scene export
def set_scene_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        rsv_version = resolver.get_rsv_task_version(**rsv_task_properties.value)
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        rsv_version.set('user', user)
        rsv_version.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'maya-scene-export',
                'start'
            )
            #
            create_scene_src = option_opt.get('create_scene_src') or False
            if create_scene_src is True:
                mya_dcc_objects.Scene.set_file_new()
                set_asset_scene_src_create(rsv_task_properties)
            #
            any_scene_file = utl_dcc_objects.OsFile(any_scene_file_path)
            if any_scene_file.get_is_exists() is True:
                if create_scene_src is False:
                    mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
                #
                _mya_fnc_scp_utility.set_export_check_run(
                    rsv_task_properties
                )
                # texture
                with_texture = option_opt.get('with_texture') or False
                if with_texture is True:
                    _mya_fnc_scp_texture.set_asset_texture_export(rsv_task_properties)
                else:
                    # texture-tx
                    with_texture_tx = option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        _mya_fnc_scp_texture.set_asset_texture_tx_export(rsv_task_properties)
                # scene
                with_scene = option_opt.get('with_scene') or False
                if with_scene is True:
                    scene_file_path = set_asset_scene_export(rsv_task_properties)
                    mya_dcc_objects.Scene.set_file_open(scene_file_path)
                # snapshot-preview
                with_snapshot_preview = option_opt.get('with_snapshot_preview') or False
                if with_snapshot_preview is True:
                    set_asset_scene_snapshot_preview_export(rsv_task_properties)
                else:
                    # render-preview
                    with_render_preview = option_opt.get('with_render_preview') or False
                    if with_render_preview is True:
                        pass
                        # set_asset_scene_render_preview_export(rsv_task_properties)
                #
                create_review_link = option_opt.get('create_review_link') or False
                if create_review_link is True:
                    set_asset_review_link_create(rsv_version)
                #
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'maya-scene-export',
                    'complete'
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'maya-scene-export-script-run',
                    u'file="{}" is non-exists'.format(any_scene_file_path)
                )


# create scene-src
def set_asset_scene_src_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    _mya_fnc_scp_utility.set_asset_workspace_create(rsv_task_properties)
    #
    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
        version=version
    )
    mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)


def set_asset_cfx_scene_src_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    _mya_fnc_scp_utility.set_asset_cfx_workspace_create(rsv_task_properties)
    #
    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
        version=version
    )
    mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)


def set_asset_look_preview_scene_scr_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    _mya_fnc_scp_utility.set_asset_look_preview_workspace_pre_create(rsv_task_properties)
    #
    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
        version=version
    )
    mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)


def set_asset_scene_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    version = rsv_task_properties.get('version')
    root = rsv_task_properties.get('dcc.root')
    #
    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
        workspace='publish',
        version=version
    )
    mya_fnc_exporters.SceneExporter(
        option=dict(
            file=scene_file_path,
            location=root,
            with_xgen_collection=True
        )
    ).set_run()
    return scene_file_path


def set_asset_camera_yml_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    camera_yml_file_path = asset_scene_query.get_camera_yml_file(
        version=version
    )
    #
    mya_fnc_exporter.CameraYamlExporter(
        option=dict(
            file=camera_yml_file_path,
            root=root
        )
    ).set_run()


def set_asset_camera_abc_persp_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    camera_abc_file_path = asset_scene_query.get_camera_presp_abc_file(
        version=version
    )
    print camera_abc_file_path


def set_asset_model_scene_import(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    branch = rsv_task_properties.get('branch')
    if branch == 'asset':
        maya_scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
            step='mod',
            task='modeling',
            workspace='publish',
            version='latest'
        )
        if maya_scene_file_path:
            mya_dcc_objects.Scene.set_file_import(maya_scene_file_path)


def set_asset_scene_snapshot_preview_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    preview_mov_file_path = asset_scene_query.get_preview_mov_file(
        workspace='publish',
        version=version
    )
    #
    mya_fnc_exporter.PreviewExporter(
        file_path=preview_mov_file_path,
        root=root,
        option=dict(
            use_render=False,
            convert_to_dot_mov=True,
        )
    ).set_run()


def set_asset_review_link_create(rsv_version):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    preview_mov_file_unit = rsv_version.get_rsv_unit(
        keyword='asset-preview-mov-file'
    )
    preview_mov_file_path = preview_mov_file_unit.get_result(
        version=rsv_version.get('version')
    )
    preview_mov_file = utl_dcc_objects.OsFile(
        preview_mov_file_path
    )
    if preview_mov_file.get_is_exists() is True:
        review_mov_file_unit = rsv_version.get_rsv_unit(
            keyword='asset-review-mov-file'
        )
        review_mov_file_path = review_mov_file_unit.get_result(
            version=rsv_version.get('version')
        )
        review_mov_file = utl_dcc_objects.OsFile(review_mov_file_path)
        if review_mov_file.get_is_exists() is False:
            preview_mov_file.set_link_to(
                review_mov_file.path
            )


def set_asset_scene_render_preview_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    preview_mov_file_path = asset_scene_query.get_preview_mov_file(
        workspace='publish',
        version=version
    )
    #
    mya_fnc_exporter.PreviewExporter(
        file_path=preview_mov_file_path,
        root=root,
        option=dict(
            use_render=True,
            convert_to_dot_mov=True,
        )
    ).set_run()


def set_scene_clear_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    clear_method_dict = {
        'clear_unused_shaders': mya_dcc_objects.Scene.set_unused_shaders_clear,
        'clear_undesd_windows': mya_dcc_objects.Scene.set_unused_windows_clear,
        'clear_unused_namespaces': mya_dcc_objects.Scene.set_unused_namespaces_clear,
        'clear_unused_names': mya_dcc_objects.Scene.set_unused_names_clear,
        'clear_unused_display_layers': mya_dcc_objects.Scene.set_unused_display_layers_clear,
        'clear_unknown_plug_ins': mya_dcc_objects.Scene.set_unknown_plug_ins_clear,
        'clear_unknown_nodes': mya_dcc_objects.Scene.set_unknown_nodes_clear,
        'clear_unload_references': mya_dcc_objects.Scene.set_unload_references_clear,
    }
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        any_scene_file = utl_dcc_objects.OsFile(any_scene_file_path)
        if any_scene_file.get_is_exists() is True:
            mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
        #
        for k, v in clear_method_dict.items():
            k_enable = option_opt.get(k) or False
            if k_enable is True:
                v()
