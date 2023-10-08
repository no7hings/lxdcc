# coding:utf-8


def set_camera_create_by_any_scene_file(option):
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
            with_camera_persp_abc = option_opt.get('with_camera_persp_abc') or False
            if with_camera_persp_abc is True:
                set_asset_camera_persp_abc_create(rsv_task_properties)


def set_asset_camera_persp_abc_create(rsv_task_properties):
    raise RuntimeError(
        'this method is removed'
    )


def set_camera_export_by_any_scene_file(option):
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
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.map_to_current(any_scene_file_path)
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
            scene_src_file = utl_dcc_objects.OsFile(any_scene_file_path)
            if scene_src_file.get_is_exists() is True:
                mya_dcc_objects.Scene.open_file(any_scene_file_path)
                #
                with_camera_main_abc = option_opt.get('with_camera_main_abc') or False
                if with_camera_main_abc is True:
                    execute_asset_camera_abc_export(rsv_version, option)


def execute_asset_camera_abc_export(rsv_version, option):
    from lxbasic import bsc_core
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    frame_range = option_opt.get('camera_main_frame_range', as_array=True)
    #
    camera_abc_file_unit = rsv_version.get_rsv_unit(
        keyword='asset-camera-main-abc-file'
    )
    camera_abc_file_path = camera_abc_file_unit.get_result(version=rsv_version.get('version'))

    mya_fnc_exporters.CameraAbcExport(
        dict(
            file=camera_abc_file_path,
            location='/camera_grp',
            frame=frame_range,
        )
    ).set_run()
