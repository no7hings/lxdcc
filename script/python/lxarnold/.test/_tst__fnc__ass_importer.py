# coding:utf-8
from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

from lxarnold.dcc import dcc_objects

f = '/data/f/cjd__wuhu__debug/test_1.ass'

s = dcc_objects.Scene()

s.set_load_from_dot_ass(f)

ms = s.universe.get_obj_type('mesh').get_objs()

for g in ms:
    print g.get_port('subdiv_iterations').get()
