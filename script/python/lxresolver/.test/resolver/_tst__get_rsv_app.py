# coding:utf-8
from lxbasic import bsc_core

import lxresolver.commands as rsv_commands

bsc_core.Log.RESULT_ENABLE = False

r = rsv_commands.get_resolver()

for i_project in [
    # 'cgm',
    'nsa_dev',
    # 'tnt'
]:

    i_rsv_project = r.get_rsv_project(project=i_project)

    i_rsv_launcher = i_rsv_project.get_rsv_app(
        application='katana4.5'
    )

    print i_rsv_launcher.get_args()

    # print i_rsv_launcher.get_command(args_execute=['-c maya'], packages_extend=['lxdcc', 'lxdcc_gui', 'lxdcc_lib', 'lxdcc_rsc', 'paper_extend_usd'])
