# coding:utf-8
import sys

from lxutil import utl_core

import lxshotgun_fnc.scripts as stg_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

utl_core.Log.set_module_result_trace(
    'lynxi-shotgun-python-run',
    'method="lxshotgun_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

stg_fnc_scripts.__dict__[key](option)
