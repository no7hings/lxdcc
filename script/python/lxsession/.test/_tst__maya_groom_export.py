# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/maya/groom-export',
        #
        file='/l/prod/cgm_dev/work/assets/chr/nn_14y_light_test/grm/groom/maya/scenes/nn_14y_light_test.grm.groom.v002.ma',
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
