# coding:utf-8
# coding:utf-8
from lxutil import utl_configure, utl_core

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)


key = 'rsv-panels/asset-loader'


import lxsession.commands as ssn_commands


ssn_commands.set_hook_execute(key)
