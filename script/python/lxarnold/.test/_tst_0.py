# coding:utf-8
from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

import lxarnold.dcc.dcc_objects as and_dcc_objects

s = and_dcc_objects.Scene(option=dict(shader_rename=True))

s.set_load_from_dot_ass('/l/prod/cjd/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v026/cache/ass/nn_gongshifu.ass')

# print s.universe.get_obj('/default__material__13').to_properties()

print s.universe.to_properties()
