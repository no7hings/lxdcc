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

    print r.get_data()
    print 'Cost', t_e - t_s


t_s = bsc_core.TimeMtd.get_timestamp()
r = bsc_objects.GainThreadsRunner()
r.run_finished.set_connect_to(post_fnc)
for i in p.get_rsv_resource_groups(
    branch='asset'
):
    j_entities = i.get_rsv_resources()
    for j_entity in j_entities:
        r.set_fnc_add(
            j_entity.get_rsv_tasks
        )

r.set_start()
# post_fnc()

# Cost 0.24870800972

