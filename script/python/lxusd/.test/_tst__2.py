# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup, usd_core

usd_setup.UsdSetup.set_environs_setup()

import lxusd.fnc.exporters as usd_fnc_exporter

color_scheme = 'asset_color'

f_src = '/l/prod/cgm/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v043/cache/usd/geo/hi.usd'

f_tgt = '/l/prod/cgm/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v043/cache/usd/display_color/{}.usda'.format(color_scheme)

s = usd_core.UsdStageOpt._set_file_open_(f_src)

usd_fnc_exporter.GeometryDisplayColorExporter(
    option=dict(
        file=f_tgt,
        location='/master',
        #
        stage_src=s,
        #
        asset_name='nn_4y',
        #
        color_seed=5,
        #
        color_scheme=color_scheme
    )
).set_run()


