# coding:utf-8
from lxbasic import bsc_core

import lxsession.commands as ssn_commands

option_hook_key = 'actions/movie-open'

o = bsc_core.ArgDictStringOpt(
    dict(
        option_hook_key='actions/movie-open',
        file='/l/prod/cgm/output/assets/chr/nn_4y_test/mod/modeling/nn_4y_test.mod.modeling.v001/render/katana-images/main/close_up.master.all.ambocc.custom.mov'
    )
)

session, execute_fnc = ssn_commands.get_option_hook_args(o.to_string())

execute_fnc()
