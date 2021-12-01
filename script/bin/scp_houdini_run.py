# coding:utf-8
import sys

from lxutil import utl_core

import lxhoudini_fnc.scripts as hou_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

utl_core.Log.set_module_result_trace(
    'lynxi-houdini-python-run',
    'method="lxhoudini_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

hou_fnc_scripts.__dict__[key](option)
