# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxarnold.operators as and_operators


f = '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/render/output/default.stats.0001.json'

o = and_operators.StatsFileOpt(
    utl_dcc_objects.OsFile(f)
)

o._test_()
