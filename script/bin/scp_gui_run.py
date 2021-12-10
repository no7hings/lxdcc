# coding:utf-8
import sys

from lxutil import utl_core

import lxgui_fnc.scripts as gui_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

utl_core.Log.set_module_result_trace(
    'lynxi-gui-python-run',
    'method="lxgui_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

gui_fnc_scripts.__dict__[key](option)
