# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold', 'lxusd', 'lxshotgun',
        'lxutil', 'lxutil_gui',
        'lxkatana', 'lxkatana_gui'
    ]
)
p.set_reload()
