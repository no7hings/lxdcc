# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-cmb-render-submit',
        #
        # file='/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma',
        file='/l/prod/cgm/work/assets/chr/nn_14y_test/srf/surfacing/maya/scenes/nn_14y_test.srf.surfacing.v004.ma',
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
