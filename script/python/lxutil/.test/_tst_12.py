# coding:utf-8
from lxutil import utl_configure, utl_core

import lxutil.objects as utl_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

task_dir_path = '/data/f/look_system_workspace'

configure = utl_objects.Configure(None, utl_configure.Data.LOOK_SYSTEM_WORKSPACE_CONFIGURE_PATH)
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
                directory.set_create()
