# coding:utf-8
from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxbasic.objects as bsc_objects

env = bsc_objects.PyEnviron_()

utl_core.Log.TRACE_RESULT_ENABLE = False

r = rsv_commands.get_resolver()

for i_project in [
    'cgm',
    'nsa_dev',
    'tnt'
]:

    i_rsv_project = r.get_rsv_project(project=i_project)

    print i_rsv_project.get_value('schemes')

    i_rsv_launcher = i_rsv_project.get_rsv_app(
        application='maya'
    )

    print i_rsv_launcher.get_command(args_execute=['-c maya'], packages_extend=['lxdcc', 'lxdcc_gui', 'lxdcc_lib', 'lxdcc_rsc', 'paper_extend_usd'])
