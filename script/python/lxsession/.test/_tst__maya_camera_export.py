# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/maya/camera-export',
        #
        file='/l/prod/cgm/work/assets/chr/bl_xiz_m/cam/camera/maya/scenes/bl_xiz_m.cam.camera.v001.ma',
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
