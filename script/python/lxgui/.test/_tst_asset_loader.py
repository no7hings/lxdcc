# coding:utf-8
from lxutil import utl_core

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

import lxsession.commands as ssn_commands; ssn_commands.set_hook_execute('rsv-panels/asset-loader')


