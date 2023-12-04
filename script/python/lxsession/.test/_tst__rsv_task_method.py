# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()

time_tag = '2022_0127_1333_36_757069'

for i_f in [
    '/l/prod/cgm_dev/publish/assets/chr/nn_14y_test/srf/surfacing/nn_14y_test.srf.surfacing.v005/scene/nn_14y_test.ma',
]:
    for j_seq, (j_option_hook_key, j_script_option) in enumerate(
        [
            ('rsv-task-methods/asset/katana/render-scene-create', {}),
        ]
    ):
        j_option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key=j_option_hook_key,
                #
                # python option
                file=i_f,
                #
                user=user, time_tag=time_tag,
                #
                td_enable=True,
                # rez_beta=True,
            )
        )
        #
        j_option_opt.update_from(
            j_script_option
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=j_option_opt.to_string()
        )


