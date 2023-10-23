# coding:utf-8
import sys

import lxlog.core as log_core

import lxshotgun_fnc.scripts as stg_fnc_scripts

argv = sys.argv

key, option = argv[1], argv[2]

log_core.Log.trace_method_result(
    'lynxi-shotgun-python-run',
    'method="lxshotgun_fnc.scripts.{}(option="{}")"'.format(
        key, option
    )
)

stg_fnc_scripts.__dict__[key](option)
