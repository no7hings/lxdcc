# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

for i_file in [
    # '/l/prod/cgm/work/assets/chr/ext_andy/mod/modeling/maya/scenes/ext_andy.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_ben/mod/modeling/maya/scenes/ext_ben.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_burk/mod/modeling/maya/scenes/ext_burk.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_erzi/mod/modeling/maya/scenes/ext_erzi.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_fuzzy/mod/modeling/maya/scenes/ext_fuzzy.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_johnny/mod/modeling/maya/scenes/ext_johnny.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_luo/mod/modeling/maya/scenes/ext_luo.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_mannequin/mod/modeling/maya/scenes/ext_mannequin.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_mike/mod/modeling/maya/scenes/ext_mike.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_owl_a/mod/modeling/maya/scenes/ext_owl_a.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_proketeriat/mod/modeling/maya/scenes/ext_proketeriat.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_suraj/mod/modeling/maya/scenes/ext_suraj.mod.modeling.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_woodpecker/mod/modeling/maya/scenes/ext_woodpecker.mod.modeling.v001.ma'
]:
    j_option_opt = bsc_core.ArgDictStringOpt(
        option=dict(
            option_hook_key='rsv-task-batchers/asset/maya/model-export',
            #
            file=i_file,
            user=bsc_core.SystemMtd.get_user_name(),
            #
            # td_enable=True,
            rez_beta=True,
        )
    )
    ssn_commands.set_option_hook_execute_by_deadline(
        option=j_option_opt.to_string()
    )
