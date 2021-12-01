# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    import lxdeadline.objects as ddl_objects

    import lxdeadline.methods as ddl_methods
    #
    utl_core.Environ.set_td_enable(True)

    resolver = rsv_commands.get_resolver()
    #
    scene_file_path = '/l/prod/cjd/publish/assets/chr/huayao/srf/surfacing/huayao.srf.surfacing.v036/scene/huayao.ma'
    #
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)

    user = utl_core.System.get_user_name()
    time_tag = utl_core.System.get_time_tag()
    #
    maya_camera_export_query = ddl_objects.DdlRsvTaskQuery(
        'maya-camera-export', rsv_task_properties
    )
    maya_camera_export = ddl_methods.DdlRsvTaskMethodRunner(
        method_option=maya_camera_export_query.get_method_option(),
        script_option=maya_camera_export_query.get_script_option(
            file=scene_file_path,
            with_camera_abc=True,
            #
            user=user, time_tag=time_tag,
        )
    )
    maya_camera_export.set_run_with_deadline()
