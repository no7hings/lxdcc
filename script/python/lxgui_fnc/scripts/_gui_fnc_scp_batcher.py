# coding:utf-8


def set_lib_asset_push(option):
    from lxbasic import bsc_core
    #
    import lxgui.fnc.methods as gui_fnc_methods
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
    time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
    #
    gui_fnc_methods.LibAssetPusher(
        project=option_opt.get('project'),
        assets=option_opt.get('assets', as_array=True),
        option=dict(
            with_system_create=option_opt.get('with_system_create') or False,
            with_system_permission_create=option_opt.get('with_system_permission_create') or False,
            #
            with_shotgun_create=option_opt.get('with_shotgun_create') or False,
            with_file_copy=option_opt.get('with_file_copy') or False,
            with_surface_publish=option_opt.get('with_surface_publish') or False,
            #
            user=user, time_tag=time_tag,
        )
    ).set_run()


def set_lib_asset_pull(option):
    from lxbasic import bsc_core
    #
    import lxgui.fnc.methods as gui_fnc_methods
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    project = option_opt.get('project')
    assets = option_opt.get('assets', as_array=True)
    #
    user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
    time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
    #
    gui_fnc_methods.LibAssetPuller(
        project=project,
        assets=assets,
        option=dict(
            with_system_create=option_opt.get('with_system_create') or False,
            with_system_permission_create=option_opt.get('with_system_permission_create') or False,
            #
            with_shotgun_create=option_opt.get('with_shotgun_create') or False,
            with_file_copy=option_opt.get('with_file_copy') or False,
            with_surface_publish=option_opt.get('with_surface_publish') or False,
            #
            user=user, time_tag=time_tag,
        )
    ).set_run()


def set_lib_assets_push(option):
    from lxbasic import bsc_core
    #
    import lxgui.fnc.methods as gui_fnc_methods
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    project = option_opt.get('project')
    assets = option_opt.get('assets', as_array=True)
    #
    user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
    time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
    #
    start_index = option_opt.get('start_index')
    end_index = option_opt.get('end_index')
    #
    gui_fnc_methods.LibAssetPusher(
        project=project,
        assets=assets[int(start_index):int(end_index)+1],
        option=dict(
            with_system_create=option_opt.get('with_system_create') or False,
            with_system_permission_create=option_opt.get('with_system_permission_create') or False,
            #
            with_shotgun_create=option_opt.get('with_shotgun_create') or False,
            with_file_copy=option_opt.get('with_file_copy') or False,
            with_surface_publish=option_opt.get('with_surface_publish') or False,
            #
            user=user, time_tag=time_tag,
        )
    ).set_run()


def set_lib_assets_pull(option):
    from lxbasic import bsc_core
    #
    import lxgui.fnc.methods as gui_fnc_methods
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    project = option_opt.get('project')
    assets = option_opt.get('assets', as_array=True)
    #
    user = option_opt.get('user') or bsc_core.SystemMtd.get_user_name()
    time_tag = option_opt.get('time_tag') or bsc_core.SystemMtd.get_time_tag()
    #
    start_index = option_opt.get('start_index')
    end_index = option_opt.get('end_index')
    #
    gui_fnc_methods.LibAssetPuller(
        project=project,
        assets=assets[int(start_index):int(end_index)+1],
        option=dict(
            with_system_create=option_opt.get('with_system_create') or False,
            with_system_permission_create=option_opt.get('with_system_permission_create') or False,
            #
            with_shotgun_create=option_opt.get('with_shotgun_create') or False,
            with_file_copy=option_opt.get('with_file_copy') or False,
            with_surface_publish=option_opt.get('with_surface_publish') or False,
            #
            user=user, time_tag=time_tag,
        )
    ).set_run()
