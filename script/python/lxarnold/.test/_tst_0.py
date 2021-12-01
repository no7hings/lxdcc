# coding:utf-8
from lxarnold import and_setup

and_setup.MtoaSetup('/apps/pg/prod/mtoa/3.3.0.2/platform-linux/maya-2019').set_run()

import lxarnold.dcc.dcc_objects as and_dcc_objects

import lxarnold.dcc.dcc_operators as and_dcc_operators

s = and_dcc_objects.Scene(option=dict(shader_rename=True))

s.set_load_from_dot_ass('/data/f/katana_ass_export/test.ass')

# s.set_load_from_dot_mtlx('/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v004/look/mtlx/nn_gongshifu.mtlx')

for i in s.universe.get_objs():
    if i.type.name == 'mesh':
        print i.get_input_port('material').get()
        print and_dcc_operators.ShapeLookOpt(i).get_properties()
        print and_dcc_operators.ShapeLookOpt(i).get_visibilities()
    else:
        print i
    # else:
    #     for port in i.get_input_ports():
    #         print port


# for i in s.universe.get_connections():
#     print i
