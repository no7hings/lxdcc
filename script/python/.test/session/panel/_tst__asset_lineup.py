# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

ssn_commands.set_option_hook_execute(
    bsc_core.ArgDictStringOpt(
        option=dict(
            option_hook_key='*/asset-lineup',
        )
    ).to_string()
)
