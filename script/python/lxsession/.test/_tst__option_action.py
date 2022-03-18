# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_configure, utl_core

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)


import lxsession.commands as ssn_commands

option_hook_key = 'actions/movie-open'

o = bsc_core.KeywordArgumentsOpt(
    dict(
        option_hook_key='actions/movie-open',
        file='/l/prod/cgm/output/assets/chr/nn_4y_test/mod/modeling/nn_4y_test.mod.modeling.v001/render/katana-images/main/close_up.master.all.ambocc.custom.mov'
    )
)

session, execute_fnc = ssn_commands.get_option_hook_args(o.to_string())

execute_fnc()
