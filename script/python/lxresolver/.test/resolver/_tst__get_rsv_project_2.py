# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

p = r.get_rsv_project(
    project='cgm'
)


def post_fnc():
    t_e = bsc_core.TimeMtd.get_timestamp()

    # print p._rsv_obj_stack.get_objects()
    print 'Cost', t_e - t_s


t_s = bsc_core.TimeMtd.get_timestamp()
for i in p.get_rsv_resource_groups(
    branch='asset'
):
    i.get_rsv_tasks()

post_fnc()


