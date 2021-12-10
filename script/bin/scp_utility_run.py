# coding:utf-8
import sys

from lxutil import utl_core

import lxutil_fnc.scripts as utl_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

utl_core.Log.set_module_result_trace(
    'gui-python-run',
    'method="lxutil_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

utl_fnc_scripts.__dict__[key](option)
