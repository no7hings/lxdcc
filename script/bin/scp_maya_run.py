# coding:utf-8
import sys

from lxbasic import bsc_core

import lxmaya_fnc.scripts as mya_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

bsc_core.Log.trace_method_result(
    'lynxi-maya-python-run',
    'method="lxmaya_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

mya_fnc_scripts.__dict__[key](option)
