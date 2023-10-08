# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxuniverse',
        'lxarnold',
        'lxutil',
        'lxkatana'
    ]
)
p.set_reload()
