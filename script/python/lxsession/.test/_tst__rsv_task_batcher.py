# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()

# time_tag = bsc_core.TimeMtd.get_time_tag()

time_tag = '2022_0124_1916_14_184314'

for i_f in [
    '/l/prod/cgm_dev/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v002.ma',
]:
    for j_seq, (j_option_hook_key, j_script_option) in enumerate(
        [
            ('rsv-task-batchers/asset/maya/model-export', {}),
        ]
    ):
        j_option_opt = bsc_core.ArgDictStringOpt(
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
        j_option_opt.update_from(j_script_option)
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=j_option_opt.to_string()
        )
