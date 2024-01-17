# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.EnvExtraMtd.set_td_enable(True)

bsc_core.EnvExtraMtd.set('PAPER_TASK_ID', '202455')

ssn_commands.set_hook_execute('desktop-tools/general-publisher')
