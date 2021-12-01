# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxobj', 'lxresolver',
        'lxarnold', 'lxusd',
        'lxutil', 'lxutil_fnc', 'lxutil_gui',
        'lxhoudini', 'lxhoudini_fnc', 'lxhoudini_gui',
    ]
)
p.set_reload()

from lxhoudini import commands

print commands.get_rsv_asset_names(role='vfx')
