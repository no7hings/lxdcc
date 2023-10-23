# coding:utf-8
from lxbasic import bsc_core

import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

p = r.get_rsv_project(
    project='cgm'
)


def post_fnc():
    t_e = bsc_core.TimeMtd.get_timestamp()
    print 'Cost', t_e - t_s
    # print r.get_data()


t_s = bsc_core.TimeMtd.get_timestamp()
r = bsc_core.TrdGainStack()
r.run_finished.connect_to(post_fnc)
for i_rsv_group in p.get_rsv_resource_groups(
    branch='asset'
):
    print i_rsv_group
    j_entities = i_rsv_group.get_rsv_resources()
    for j_entity in j_entities:
        r.register(
            j_entity.get_rsv_tasks
        )

r.start()
# post_fnc()

# Cost 0.24870800972

