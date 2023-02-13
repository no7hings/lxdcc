# coding:utf-8
import sys

from lxmaya_fnc.scripts import _mya_fnc_scp_utility, _mya_fnc_scp_texture, _mya_fnc_scp_scene


def set_look_export_by_any_scene_file(option):
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
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    option_opt = bsc_core.ArgDictStringOpt(option, default_option='with_look_ass=True')
    #
    scene_src_file_path = option_opt.get('file')
    scene_src_file_path = utl_core.Path.set_map_to_platform(scene_src_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        #
        force = option_opt.get('force') or False
        #
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            scene_src_file = utl_dcc_objects.OsFile(scene_src_file_path)
            if scene_src_file.get_is_exists() is True:
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'maya-look-export',
                    'start'
                )
                #
                mya_dcc_objects.Scene.set_file_open(scene_src_file_path)
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
                #
                with_look_ass = option_opt.get('with_look_ass') or False
                if with_look_ass is True:
                    set_asset_look_ass_export(rsv_task_properties, force)
                #
                with_look_yml = option_opt.get('with_look_yml') or False
                if with_look_yml is True:
                    set_asset_look_preview_yml_export(rsv_task_properties)
                #
                with_look_properties_usd = option_opt.get('with_look_properties_usd') or False
                if with_look_properties_usd is True:
                    set_asset_look_properties_usd_export(rsv_task_properties)
                #
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'maya-look-export',
                    'complete'
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'maya-look-export-script-run',
                    u'file="{}" is non-exists'.format(scene_src_file_path)
                )
    else:
        utl_core.Log.set_module_warning_trace(
            key,
            u'file="{}" is not available'.format(scene_src_file_path)
        )


def set_asset_look_ass_export(rsv_task_properties, force=False):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    workspace = rsv_task_properties.get('workspace')
    task = rsv_task_properties.get('task')
    version = rsv_task_properties.get('version')
    #
    root = rsv_task_properties.get('dcc.root')
    root_dcc_dag_path = bsc_core.DccPathDagOpt(root)
    root_mya_dag_path = root_dcc_dag_path.set_translate_to(ma_configure.Util.OBJ_PATHSEP)
    root_mya_obj = mya_dcc_objects.Group(root_mya_dag_path.value)
    if root_mya_obj.get_is_exists() is True:
        _look_pass_names = root_mya_obj.get_port('pg_lookpass').get_enumerate_strings() or None
        if _look_pass_names is not None:
            look_pass_names = _look_pass_names
        else:
            look_pass_names = ['default']
        # sequence-file(s) export per frame
        start_frame, end_frame = (
            root_mya_obj.get_port('pg_start_frame').get(),
            root_mya_obj.get_port('pg_end_frame').get()
        )
        # export per look-pass
        for i_look_pass_name in look_pass_names:
            root_mya_obj.get_port('pg_lookpass').set(i_look_pass_name)
            if workspace == 'work':
                look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_work_file(
                    task=task,
                    version=version
                )
            elif workspace == 'publish':
                look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_file(
                    task=task,
                    version=version
                )
            else:
                raise RuntimeError(
                    'workspace="{}" is not available'.format(workspace)
                )
            #
            i_look_ass_file = utl_dcc_objects.OsFile(look_ass_file_path)
            i_path_base, i_ext = i_look_ass_file.path_base, i_look_ass_file.ext
            if i_look_pass_name == 'default':
                i_look_ass_file_path = look_ass_file_path
            else:
                i_look_ass_file_path = '{}.{}{}'.format(i_path_base, i_look_pass_name, i_ext)
            # main-file(s)
            if i_look_ass_file.get_is_exists() is False or force is True:
                mya_fnc_exporters.LookAssExporter(
                    option=dict(
                        file=i_look_ass_file_path,
                        location=root,
                        texture_use_environ_map=True,
                    )
                ).set_run()
            #
            if start_frame is not None and end_frame is not None:
                i_frame = start_frame, end_frame
                #
                mya_fnc_exporters.LookAssExporter(
                    option=dict(
                        file=i_look_ass_file_path,
                        location=root,
                        frame=i_frame,
                        texture_use_environ_map=True,
                    )
                ).set_run()
    else:
        utl_core.Log.set_module_warning_trace(
            key,
            'obj="{}" is non-exists'.format(root_mya_obj.path)
        )


def set_asset_look_preview_yml_export(rsv_task_properties):
    from lxutil import utl_core
    #
    import lxobj.objects as core_objects
    #
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    workspace = rsv_task_properties.get('workspace')
    task = rsv_task_properties.get('task')
    version = rsv_task_properties.get('version')
    #
    root = rsv_task_properties.get('dcc.root')
    root_dcc_dag_path = core_objects.ObjDagPath(root)
    root_mya_dag_path = root_dcc_dag_path.set_translate_to(ma_configure.Util.OBJ_PATHSEP)
    root_mya_obj = mya_dcc_objects.Group(root_mya_dag_path.path)
    if root_mya_obj.get_is_exists() is True:
        if workspace == 'work':
            look_yaml_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_work_yml_file(
                task=task,
                version=version
            )
        elif workspace == 'publish':
            look_yaml_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_yml_file(
                task=task,
                version=version
            )
        else:
            raise TypeError()
        #
        mya_fnc_exporters.LookYamlExporter(
            option=dict(
                file=look_yaml_file_path,
                root=root
            )
        ).set_run()
    else:
        utl_core.Log.set_module_warning_trace(
            key,
            'obj="{}" is non-exists'.format(root)
        )


def set_asset_look_properties_usd_export(rsv_task_properties):
    import lxutil_fnc.scripts as utl_fnc_scripts
    #
    utl_fnc_scripts.set_asset_look_properties_usd_export(
        rsv_task_properties
    )


# import
def set_look_import_by_any_scene_file(option):
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
    option_opt = bsc_core.ArgDictStringOpt(option, default_option='with_look_ass=True')
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
        step = rsv_task_properties.get('step')
        if branch == 'asset':
            if step in ['mod', 'srf', 'rig']:
                with_scene = option_opt.get('with_scene')
                if with_scene is True:
                    mya_dcc_objects.Scene.set_file_open(scene_file_path)
                #
                with_look_preview = option_opt.get('with_look_preview') or False
                if with_look_preview is True:
                    set_asset_look_preview_import(rsv_task_properties)
                #
                if with_scene is True:
                    version = rsv_task_properties.get('version')
                    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(wokspace='publish', version=version)
                    utl_dcc_objects.OsFile(scene_file_path).set_backup()
                    mya_dcc_objects.Scene.set_file_save_to(scene_file_path)


def set_asset_look_preview_import(rsv_task_properties):
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxmaya.fnc.builders as mya_fnc_builders
    #
    branch = rsv_task_properties.get('branch')
    step = rsv_task_properties.get('step')
    if branch == 'asset':
        if step in ['mod', 'srf', 'rig']:
            project = rsv_task_properties.get('project')
            asset = rsv_task_properties.get('asset')
            #
            mya_fnc_builders.AssetBuilder(
                option=dict(
                    project=project,
                    asset=asset,
                    #
                    with_surface_geometry_uv_map=True,
                    with_surface_look_preview=True,
                )
            ).set_run()
            #
            mya_dcc_objects.TextureReferences.set_files_value_repair()


def set_cfx_look_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            version = rsv_task_properties.get('version')
            #
            create_scene_src = option_opt.get('create_scene_src') or False
            if create_scene_src is True:
                result = _mya_fnc_scp_utility.set_asset_cfx_workspace_create(rsv_task_properties)
                if result is True:
                    mya_dcc_objects.Scene.set_file_new()
                    result = _mya_fnc_scp_utility.set_asset_cfx_workspace_create(rsv_task_properties)
                    if result is True:
                        scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
                            version=version
                        )
                        mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)
            #
            any_scene_file = utl_dcc_objects.OsFile(any_scene_file_path)
            if any_scene_file.get_is_exists() is True:
                mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
                #
                with_texture = option_opt.get('with_texture') or False
                if with_texture is True:
                    _mya_fnc_scp_texture.set_asset_texture_export(
                        rsv_task_properties
                    )
                #
                with_scene = option_opt.get('with_scene') or False
                if with_scene is True:
                    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
                        version=version
                    )
                    mya_dcc_objects.Scene.set_file_save_to(scene_file_path)


def set_look_preview_export_by_any_scene_file(option):
    # /l/prod/lib/publish/assets/chr/ast_cjd_didi/srf/surfacing/ast_cjd_didi.srf.surfacing.v001/scene/ast_cjd_didi.ma
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
    import lxresolver.operators as rsv_operators
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    option_opt = bsc_core.ArgDictStringOpt(option, default_option='with_look_ass=True')
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        #
        force = option_opt.get('force') or False
        #
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        step = rsv_task_properties.get('step')
        task = rsv_task_properties.get('task')
        if branch == 'asset':
            create_scene_src = option_opt.get('create_scene_src') or False
            if create_scene_src is True:
                mya_dcc_objects.Scene.set_file_new()
                _mya_fnc_scp_utility.set_asset_look_preview_workspace_pre_create(rsv_task_properties)
                #
                mya_dcc_objects.Scene.set_file_save_to(
                    any_scene_file_path
                )
            else:
                any_scene_file = utl_dcc_objects.OsFile(any_scene_file_path)
                if any_scene_file.get_is_exists() is True:
                    mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
                else:
                    raise IOError(
                        utl_core.Log.set_module_error_trace(
                            'look-preview-export',
                            'file="{}" is non-exists'.format(any_scene_file_path)
                        )
                    )
            #
            set_asset_look_preview_workspace_post_create(rsv_task_properties)
            #
            with_scene = option_opt.get('with_scene') or False
            if with_scene is True:
                _mya_fnc_scp_scene.set_asset_scene_export(rsv_task_properties)
            #
            with_work_scene_src = option_opt.get('with_work_scene_src') or False
            if with_work_scene_src is True:
                set_asset_look_preview_work_scene_src_create(rsv_task_properties)


def set_asset_look_preview_workspace_post_create(rsv_task_properties):
    import lxresolver.commands as rsv_commands
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    resolver = rsv_commands.get_resolver()
    rsv_task = resolver.get_rsv_task(
        **rsv_task_properties.value
    )
    #
    texture_directory_unit = rsv_task.get_rsv_unit(
        keyword='asset-texture-tgt-dir'
    )
    #
    texture_directory_path = texture_directory_unit.get_result(version=version)
    #
    mya_fnc_exporters.TextureBaker(
        option=dict(
            directory=texture_directory_path,
            location='/master/hi',
            resolution=2048,
            aa_samples=3
        )
    ).set_run()
    #
    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
        version=version
    )
    mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)


def set_asset_look_preview_work_scene_src_create(rsv_task_properties):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
        version=version
    )
    latest_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_work_maya_src_file(
        version='latest'
    )
    if latest_scene_src_file_path:
        if bsc_core.StgPathLinkMtd.get_is_link_source_to(
            scene_file_path, latest_scene_src_file_path
        ) is False:
            work_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_work_maya_src_file(
                version='new'
            )
            #
            utl_dcc_objects.OsFile(
                scene_file_path
            ).set_link_to(work_scene_src_file_path)
        else:
            utl_core.Log.set_module_warning_trace(
                'preview work-scene-src link create',
                u'link="{}" >> "{}" is exists'.format(
                    scene_file_path, latest_scene_src_file_path
                )
            )
