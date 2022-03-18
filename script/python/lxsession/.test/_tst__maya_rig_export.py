# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

for i_file_path in [
    '/l/prod/cgm/work/assets/chr/ext_andy/rig/rigging/maya/scenes/ext_andy.rig.rigging.v001.ma'
]:
    j_option_opt = bsc_core.KeywordArgumentsOpt(
        option=dict(
            option_hook_key='rsv-task-batchers/asset/maya/rig-export',
            #
            file=i_file_path,
            user=bsc_core.SystemMtd.get_user_name(),
            #
            td_enable=True,
            # rez_beta=True,
        )
    )
    #
    ssn_commands.set_option_hook_execute_by_deadline(
        option=j_option_opt.to_string()
    )
