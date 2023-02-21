# coding:utf-8
from lxbasic import bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()

time_tag = bsc_core.TimeMtd.get_time_tag()

for i_f in [
    # '/l/prod/xkt/publish/assets/chr/jiguang/srf/srf_anishading/jiguang.srf.srf_anishading.v006/scene/jiguang.ma',
    # '/l/prod/xkt/publish/assets/chr/heidong/srf/srf_anishading/heidong.srf.srf_anishading.v015/scene/heidong.ma'
    '/l/prod/cgm/publish/assets/chr/nn_4y_test/srf/srf_anishading/nn_4y_test.srf.srf_anishading.v001/scene/nn_4y_test.ma',
]:
    for j_seq, (j_option_hook_key, j_script_option) in enumerate(
        [
            ('rsv-task-methods/asset/maya/look-preview-export', {}),
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
                rez_beta=True,
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


