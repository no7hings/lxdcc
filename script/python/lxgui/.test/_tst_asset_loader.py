# coding:utf-8
from lxutil import utl_core

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

import lxgui_fnc.scripts as gui_fnc_scripts; gui_fnc_scripts.set_session_hook_run('rsv-panels/asset-batcher')
