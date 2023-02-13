# coding:utf-8
from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxbasic.objects as bsc_objects

env = bsc_objects.PyEnviron_()
# env.LYNXI_RESOLVER_CONFIGURES += '/data/e/myworkspace/td/lynxi/script/configure/resolver/default', '/data/e/myworkspace/td/lynxi/script/configure/resolver/new'

utl_core.Log.TRACE_RESULT_ENABLE = False

r = rsv_commands.get_resolver()

for i_project in [
    # 'cgm',
    'nsa_dev'
]:

    i_rsv_project = r.get_rsv_project(project=i_project)

    for j_shot in i_rsv_project.get_rsv_resources(
        branch='shot',
    ):
        print j_shot


