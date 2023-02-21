# coding:utf-8
from lxbasic import bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()

time_tag = '2022_0127_1333_36_757069'

for i_f in [
    '/l/prod/cgm_dev/publish/assets/chr/nn_14y_test/srf/surfacing/nn_14y_test.srf.surfacing.v005/scene/nn_14y_test.ma',
]:
    for j_seq, (j_option_hook_key, j_script_option) in enumerate(
        [
            # ('rsv-task-methods/asset/maya/scene-clear', dict(clear_unused_shaders=True)),
            # ('rsv-task-methods/asset/shotgun/shotgun-create', {}),
            # ('rsv-task-methods/asset/maya/scene-export', dict(create_review_link=True)),
            # ('rsv-task-methods/asset/maya/geometry-export', {}),
            # ('rsv-task-methods/asset/maya/look-export', {}),
            # ('rsv-task-methods/asset/maya/look-preview-export', {}),
            # ('rsv-task-methods/asset/maya/camera-export', {}),
            # ('rsv-task-methods/asset/usd/usd-create', dict(dependencies=['rsv-task-methods/asset/maya/geometry-export'])),
            # ('rsv-task-methods/asset/maya/test', {}),
            # ('rsv-task-methods/asset/shotgun/shotgun-export', {}),
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
        j_option_opt.set_update(
            j_script_option
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=j_option_opt.to_string()
        )


