# coding:utf-8


key = 'rsv-panels/asset-loader'


import lxsession.commands as ssn_commands


ssn_commands.set_option_hook_execute_by_shell(
    'hook_key={}'.format(key)
)
