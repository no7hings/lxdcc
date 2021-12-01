# coding:utf-8
import sys

from lxutil import utl_core

import lxmaya_fnc.scripts as mya_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

utl_core.Log.set_module_result_trace(
    'lynxi-maya-python-run',
    'method="lxmaya_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

mya_fnc_scripts.__dict__[key](option)
