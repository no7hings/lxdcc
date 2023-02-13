# coding:utf-8


def set_asset_method_batch_run(option):
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
            scene_src_file_unit = rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
            scene_src_file_path = scene_src_file_unit.get_result(version='latest')
            if scene_src_file_path is not None:
                script = option_opt.get('script')
                if script == 'maya_camera_export':
                    set_maya_camera_export(option='file={}'.format(scene_src_file_path))
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset-maya-export',
                    '"work-scene-src-file" is non-exists'
                )


def set_maya_camera_export(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxdeadline.objects as ddl_objects
    #
    import lxdeadline.methods as ddl_methods
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_src_file_path = option_opt.get('file')
    #
    resolver = rsv_commands.get_resolver()
    #
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_src_file_path)
    if rsv_task_properties:
        #
        user = utl_core.System.get_user_name()
        time_tag = utl_core.System.get_time_tag()
        maya_camera_export_query = ddl_objects.DdlRsvTaskQuery(
            'maya-camera-export', rsv_task_properties
        )
        maya_camera_exporter = ddl_methods.RsvTaskHookExecutor(
            method_option=maya_camera_export_query.get_method_option(),
            script_option=maya_camera_export_query.get_script_option(
                file=any_scene_src_file_path,
                with_camera_persp_abc=True,
                #
                user=user, time_tag=time_tag,
            )
        )
        maya_camera_exporter.set_run_with_deadline()
