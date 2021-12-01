# coding:utf-8
import sys

from lxutil import utl_core

import lxkatana_fnc.scripts as ktn_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

utl_core.Log.set_module_result_trace(
    'lynxi-katana-python-run',
    'method="lxkatana_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

ktn_fnc_scripts.__dict__[key](option)
