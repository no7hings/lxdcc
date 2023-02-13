# coding:utf-8
import lxbasic.objects as bsc_objects

from lxutil import utl_configure

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxresolver.commands as rsv_commands

from lxutil_fnc.dcc.dcc_objects import _utl_fnc_dcc_obj_utility, _utl_fnc_dcc_obj_callback


def set_scene_load_from_configure(configure_file_path):
    scene = _utl_fnc_dcc_obj_utility.Scene()
    scene.set_load_from_configure(configure_file_path)
    _utl_fnc_dcc_obj_callback.__dict__['SCENE'] = scene
    return scene


def set_scene_load_from_configure_(configure_file_path):
    scene = _utl_fnc_dcc_obj_utility.Scene()
    scene.set_load_from_configure_(configure_file_path)
    _utl_fnc_dcc_obj_callback.__dict__['SCENE'] = scene
    return scene


def set_surface_system_workspace_open(task_properties):
    branch = task_properties.get('branch')
    step = task_properties.get('step')
    if branch == 'asset' and step == 'srf':
        resolver = rsv_commands.get_resolver()
        #
        rsv_task = resolver.get_rsv_task(**task_properties.value)
        keyword = 'asset-source-task-dir'.format(**task_properties.value)
        #
        task_dir = rsv_task.get_rsv_unit(
            keyword=keyword, workspace='work'
        )
        if task_dir:
            task_dir_path = task_dir.get_result(version='latest')
            if task_dir_path:
                task_directory = utl_dcc_objects.OsDirectory_(task_dir_path)
                if task_directory.get_is_exists():
                    task_directory.set_open()


def set_surface_system_workspace_create(task_properties):
    branch = task_properties.get('branch')
    step = task_properties.get('step')
    #
    create_list = []
    if branch == 'asset' and step == 'srf':
        resolver = rsv_commands.get_resolver()
        rsv_task = resolver.get_rsv_task(**task_properties.value)
        keyword = 'asset-source-task-dir'.format(**task_properties.value)
        #
        task_dir = rsv_task.get_rsv_unit(
            keyword=keyword, workspace='work'
        )
        if task_dir:
            task_dir_path = task_dir.get_result(version='latest')
            if task_dir_path:
                configure = bsc_objects.Configure(value=utl_configure.Data.LOOK_SYSTEM_WORKSPACE_CONFIGURE_PATH)
                configure.set('option.root', task_dir_path)
                configure.set_flatten()
                keys = configure.get_branch_keys('workspace')
                for key in keys:
                    enable = configure.get('workspace.{}.enable'.format(key))
                    if enable is True:
                        directory_paths = configure.get('workspace.{}.directories'.format(key)) or []
                        for directory_path in directory_paths:
                            directory = utl_dcc_objects.OsDirectory_(directory_path)
                            if directory.get_is_exists() is False:
                                create_list.append(directory)
    #
    utl_core.Log.set_module_result_trace(
        'system-workspace create',
        'start'
    )
    if create_list:
        ps = utl_core.Progress.set_create(len(create_list))
        for directory in create_list:
            utl_core.Progress.set_update(ps)
            directory.set_create()
        utl_core.Progress.set_stop(ps)
    #
    utl_core.Log.set_module_result_trace(
        'system-workspace create',
        'complete'
    )
