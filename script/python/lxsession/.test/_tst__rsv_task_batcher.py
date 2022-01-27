# coding:utf-8
# coding:utf-8
import os

from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

# os.environ['LYNXI_RESOURCES'] += os.pathsep + '/data/e/myworkspace/td/lynxi/script/python/.resources'

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

# time_tag = bsc_core.SystemMtd.get_time_tag()

time_tag = '2022_0124_1916_14_184314'

for i_f in [
    '/l/prod/cgm_dev/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v002.ma',
]:
    for j_seq, (j_option_hook_key, j_script_option) in enumerate(
        [
            ('rsv-task-batchers/asset/maya/model-export', {}),
        ]
    ):
        j_option_opt = bsc_core.KeywordArgumentsOpt(
            option=dict(
                option_hook_key=j_option_hook_key,
                #
                file=i_f,
                user=bsc_core.SystemMtd.get_user_name(),
                #
                td_enable=True,
                # rez_beta=True,
            )
        )
        #
        j_option_opt.set_update(
            j_script_option
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=j_option_opt.to_string()
        )
