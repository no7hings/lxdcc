# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxarnold.operators as and_operators


f = '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/output/default.profile.0001.json'

o = and_operators.ProfileFileOpt(
    utl_dcc_objects.OsFile(f)
)

o._test_()
