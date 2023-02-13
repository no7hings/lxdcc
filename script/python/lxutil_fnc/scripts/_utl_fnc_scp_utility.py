# coding:utf-8


def set_maya_asset_task_batch_run_(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    project = option_opt.get('project')
    step = option_opt.get('step')
    task = option_opt.get('task')
    #
    resolver = rsv_commands.get_resolver()
    rsv_project = resolver.get_rsv_project(project=project)
    #
    rsv_entities = rsv_project.get_rsv_resources(**option_opt.value)
    for rsv_entity in rsv_entities:
        rsv_task = rsv_entity.get_rsv_task(step=step, task=task)
        if rsv_task is not None:
            work_maya_scene_src_file_unit = rsv_task.get_rsv_unit(keyword='asset-source-maya-scene-src-file')
            work_maya_scene_src_file_path = work_maya_scene_src_file_unit.get_result(version='latest')
            if work_maya_scene_src_file_path is not None:
                set_asset_export_by_work_maya_scene_src_file(
                    option='file={}'.format(work_maya_scene_src_file_path)
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset-maya-export',
                    '"work-scene-src-file" is non-exists'
                )


def set_asset_export_by_work_maya_scene_src_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    work_scene_src_file_path = option_opt.get('file')
    #
    resolver = rsv_commands.get_resolver()
    #
    rsv_task = resolver.get_rsv_task_by_any_file_path(work_scene_src_file_path)
    #
    if rsv_task is not None:
        work_maya_scene_src_file = utl_dcc_objects.OsFile(work_scene_src_file_path)
        #
        maya_scene_src_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-maya-scene-src-file')
        maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-maya-scene-file')
        maya_scene_src_file_path = maya_scene_src_file_rsv_unit.get_result(version='latest')
        if maya_scene_src_file_path is not None:
            maya_scene_src_file = utl_dcc_objects.OsFile(maya_scene_src_file_path)
            if work_maya_scene_src_file.get_timestamp_is_same_to(maya_scene_src_file) is True:
                utl_core.Log.set_module_warning_trace(
                    'asset-maya-export',
                    u'file="{}" is non-changed'.format(maya_scene_src_file_path)
                )
                maya_scene_file_path = maya_scene_file_rsv_unit.get_result(
                    version=maya_scene_src_file_rsv_unit.get_latest_version()
                )
                if utl_dcc_objects.OsFile(
                        maya_scene_file_path
                ).get_is_exists_file() is True:
                    return
                else:
                    set_asset_publish_by_maya_scene_src(
                        option='file={}'.format(maya_scene_src_file_path)
                    )
                return
        #
        version_rsv_unit = rsv_task.get_rsv_unit(
            keyword='{branch}-release-version-dir'
        )
        new_version = version_rsv_unit.get_new_version()
        #
        maya_scene_src_file_path = maya_scene_src_file_rsv_unit.get_result(version=new_version)
        work_maya_scene_src_file.set_copy_to_file(maya_scene_src_file_path)
        set_asset_publish_by_maya_scene_src(
            option='file={}'.format(maya_scene_src_file_path)
        )


def set_asset_publish_by_maya_scene_src(option):
    from lxbasic import bsc_core
    #
    import lxutil_fnc.objects as utl_fnc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    maya_scene_src_file_path = option_opt.get('file')
    #
    user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
    time_tag = option_opt.get('time_tag') or bsc_core.TimeMtd.get_time_tag()
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(maya_scene_src_file_path)
    if rsv_task_properties:
        rsv_task_properties.set('option.version', rsv_task_properties.get('version'))
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        methods_loader = utl_fnc_objects.TaskMethodsLoader(rsv_task_properties)
        entity_path = methods_loader.get_entity_obj_path()
        method_paths = methods_loader.get_entity_method_obj_paths(entity_path)
        if method_paths:
            sorted_method_paths = methods_loader.get_sorted_objs(method_paths)
            for i_method_path in sorted_method_paths:
                i_method = methods_loader.get_method(i_method_path)
                if i_method is not None:
                    i_method._set_export_debug_run_(use_window=False)


def set_fnc_methods_run_by_assets_katana_scene_src(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    project = option_opt.get('project')
    step = option_opt.get('step')
    task = option_opt.get('task')
    #
    resolver = rsv_commands.get_resolver()
    rsv_project = resolver.get_rsv_project(project=project)
    #
    rsv_entities = rsv_project.get_rsv_resources(**option_opt.value)
    for rsv_entity in rsv_entities:
        rsv_task = rsv_entity.get_rsv_task(step=step, task=task)
        if rsv_task is not None:
            katana_scene_src_src_file_unit = rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
            katana_scene_src_src_file_path = katana_scene_src_src_file_unit.get_result(version='latest')
            if katana_scene_src_src_file_path:
                set_asset_publish_by_katana_scene_src(
                    option='file={}'.format(katana_scene_src_src_file_path)
                )


def set_asset_publish_by_katana_scene_src(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil_fnc.objects as utl_fnc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    katana_scene_src_file_path = option_opt.get('file')
    #
    user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
    time_tag = option_opt.get('time_tag') or bsc_core.TimeMtd.get_time_tag()
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(katana_scene_src_file_path)
    if rsv_task_properties:
        rsv_task_properties.set('option.version', rsv_task_properties.get('version'))
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        methods_loader = utl_fnc_objects.TaskMethodsLoader(rsv_task_properties)
        entity_path = methods_loader.get_entity_obj_path()
        method_paths = methods_loader.get_entity_method_obj_paths(entity_path)
        sorted_method_paths = methods_loader.get_sorted_objs(method_paths)
        if sorted_method_paths:
            g_p = utl_core.GuiProgressesRunner(maximum=len(sorted_method_paths))
            for i_method_path in sorted_method_paths:
                g_p.set_update()
                i_method = methods_loader.get_method(i_method_path)
                if i_method is not None:
                    i_method._set_export_debug_run_()
            #
            g_p.set_stop()


def set_copy_publish_to_work_batch_run(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    project = option_opt.get('project')
    step = option_opt.get('step')
    task = option_opt.get('task')
    #
    resolver = rsv_commands.get_resolver()
    rsv_project = resolver.get_rsv_project(project=project)
    #
    rsv_entities = rsv_project.get_rsv_resources(**option_opt.value)
    for rsv_entity in rsv_entities:
        rsv_task = rsv_entity.get_rsv_task(step=step, task=task)
        if rsv_task is not None:
            katana_scene_src_file_unit = rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
            katana_scene_src_file_path = katana_scene_src_file_unit.get_result(version='latest')
            if katana_scene_src_file_path is not None:
                work_katana_scene_src_file_unit = rsv_task.get_rsv_unit(keyword='asset-source-katana-scene-src-file')
                work_katana_scene_src_file_path = work_katana_scene_src_file_unit.get_result()
                if work_katana_scene_src_file_path is None:
                    new_work_katana_scene_src_file_path = work_katana_scene_src_file_unit.get_result(version='v001')
                else:
                    new_work_katana_scene_src_file_path = work_katana_scene_src_file_unit.get_result(version='new')
                #
                print katana_scene_src_file_path, new_work_katana_scene_src_file_path
                if utl_dcc_objects.OsFile(katana_scene_src_file_path).get_timestamp_is_same_to(
                    utl_dcc_objects.OsFile(work_katana_scene_src_file_path)
                ):
                    continue
                #
                # utl_dcc_objects.OsFile(katana_scene_src_file_path).set_copy_to_file(
                #     new_work_katana_scene_src_file_path
                # )
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset-maya-export',
                    '"work-scene-src-file" is non-exists'
                )


def set_work_file_repair_batch_run(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    project = option_opt.get('project')
    step = option_opt.get('step')
    task = option_opt.get('task')
    #
    resolver = rsv_commands.get_resolver()
    rsv_project = resolver.get_rsv_project(project=project)
    #
    rsv_entities = rsv_project.get_rsv_resources(**option_opt.value)
    for rsv_entity in rsv_entities:
        rsv_task = rsv_entity.get_rsv_task(step=step, task=task)
        if rsv_task is not None:
            work_katana_scene_src_file_unit = rsv_task.get_rsv_unit(keyword='asset-source-katana-scene-src-file')
            work_katana_scene_src_file_path = work_katana_scene_src_file_unit.get_result()
            if work_katana_scene_src_file_path:
                set_work_file_repair('file={}'.format(work_katana_scene_src_file_path))
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset-maya-export',
                    '"work-scene-src-file" is non-exists'
                )


def set_work_file_repair(option):
    from lxbasic import bsc_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    work_katana_scene_src_file_path = option_opt.get('file')
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(work_katana_scene_src_file_path)
    if rsv_task_properties:
        utl_dcc_objects.OsFile(work_katana_scene_src_file_path).set_backup()
        #
        ktn_dcc_objects.Scene.set_file_open(work_katana_scene_src_file_path)
        #
        work_texture_dir_Path = rsv_operators.RsvAssetTextureQuery(rsv_task_properties).get_work_directory(version='new')
        #
        utl_dcc_operators.DccTexturesOpt(
            ktn_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_copy_and_repath_to(work_texture_dir_Path)
        #
        ktn_dcc_objects.Scene.set_file_save()
