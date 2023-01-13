# coding:utf-8
import lxbasic.objects as bsc_object

import lxutil.dcc.dcc_objects as utl_dcc_objects

p = bsc_object.PyReloader(['lxbasic', 'lxutil'])

f = utl_dcc_objects.OsFile('/data/f/aaa.obj')

print p.get_requires_graph()

p.set_reload()
