# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
reload(utl_dcc_objects)

p = utl_dcc_objects.PyReloader(['lxutil', 'lxhoudini'])

p.set_reload()

from lxhoudini import hou_core

s = hou_core.HouObj()

s._test()
