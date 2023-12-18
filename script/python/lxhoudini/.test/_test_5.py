# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.PyReloader(['lxutil', 'lxhoudini'])

p.set_reload()

from lxhoudini import hou_core

s = hou_core.HouObj()

s._test()
