# coding:utf-8
import sys

from lxbasic import bsc_core

import lxutil_fnc.scripts as utl_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

bsc_core.Log.trace_method_result(
    'gui-python-run',
    'method="lxutil_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

utl_fnc_scripts.__dict__[key](option)
