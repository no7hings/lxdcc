# coding:utf-8
import sys

from lxbasic import bsc_core

import lxhoudini_fnc.scripts as hou_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

bsc_core.Log.trace_method_result(
    'lynxi-houdini-python-run',
    'method="lxhoudini_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

hou_fnc_scripts.__dict__[key](option)
