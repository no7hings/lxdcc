# coding:utf-8
from lxbasic import bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SystemMtd.get_user_name()


for i_f in [
    '/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma',
]:
    for j_seq, (j_option_hook_key, j_script_option) in enumerate(
        [
            ('rsv-task-methods/asset/rv/movie-convert', {}),
        ]
    ):
        j_option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key=j_option_hook_key,
                #
                file=i_f,
                user=bsc_core.SystemMtd.get_user_name(),
                time_tag=bsc_core.TimeMtd.get_time_tag(),
                #
                image_file='/l/prod/cgm/output/assets/chr/nn_14y_test/mod/modeling/nn_14y_test.mod.modeling.v002/render/katana-images/main/full_body.master.all.plastic.custom/beauty.####.exr',
                movie_file='/l/prod/cgm/output/assets/chr/nn_14y_test/mod/modeling/nn_14y_test.mod.modeling.v002/render/katana-images/main/full_body.master.all.plastic.custom.mov',
                #
                option_hook_key_extend=['full_body-master-all-plastic-custom'],
                #
                start_frame=1001,
                end_frame=1240,
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
