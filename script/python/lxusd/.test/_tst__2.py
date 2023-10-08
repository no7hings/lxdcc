# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup, usd_core

usd_setup.UsdSetup.build_environ()

import lxusd.fnc.exporters as usd_fnc_exporter

color_scheme = 'shell_color'

dir_ = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v056/cache/usd'

f_src = '{}/geo/hi.usd'.format(dir_)

f_tgt = '{}/geo_extra/{}.usd'.format(dir_, color_scheme)

s = usd_core.UsdStageOpt._open_file_(f_src)

usd_fnc_exporter.GeometryDisplayColorExporter(
    option=dict(
        file=f_tgt,
        location='/master',
        #
        stage_src=s,
        #
        asset_name='td_test',
        #
        color_seed=5,
        #
        color_scheme=color_scheme
    )
).set_run()


