# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

for i_file_path in [
    # '/l/prod/cgm/work/assets/chr/ext_andy/rig/rigging/maya/scenes/ext_andy.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_ben/rig/rigging/maya/scenes/ext_ben.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_burk/rig/rigging/maya/scenes/ext_burk.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_erzi/rig/rigging/maya/scenes/ext_erzi.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_fuzzy/rig/rigging/maya/scenes/ext_fuzzy.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_johnny/rig/rigging/maya/scenes/ext_johnny.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_luo/rig/rigging/maya/scenes/ext_luo.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_mannequin/rig/rigging/maya/scenes/ext_mannequin.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_mike/rig/rigging/maya/scenes/ext_mike.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_owl_a/rig/rigging/maya/scenes/ext_owl_a.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_proketeriat/rig/rigging/maya/scenes/ext_proketeriat.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_suraj/rig/rigging/maya/scenes/ext_suraj.rig.rigging.v001.ma',
    # '/l/prod/cgm/work/assets/chr/ext_woodpecker/rig/rigging/maya/scenes/ext_woodpecker.rig.rigging.v001.ma',
    '/l/prod/cgm_dev/work/assets/chr/nn_14y_test/rig/rigging/maya/scenes/nn_14y_test.rig.rigging.v001.ma'
]:
    j_option_opt = bsc_core.KeywordArgumentsOpt(
        option=dict(
            option_hook_key='rsv-task-batchers/asset/gen-rig-export',
            #
            choice_scheme='asset-maya-output',
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
