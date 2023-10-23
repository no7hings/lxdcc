# coding:utf-8
from lxbasic import bsc_core

import lxresolver.commands as rsv_commands

bsc_core.Log.RESULT_ENABLE = False

r = rsv_commands.get_resolver()

for i_project in [
    'cgm',
    'nsa_dev'
]:
    i_rsv_project = r.get_rsv_project(project=i_project)

    print i_rsv_project.get_dcc_data('maya')
