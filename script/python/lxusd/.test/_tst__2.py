# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.set_environs_setup()

import lxusd.fnc.exporters as usd_fnc_exporter

f_src = '/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/nn_4y.srf.surfacing.v075/cache/usd/nn_4y.usda'

f_tgt = '/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/nn_4y.srf.surfacing.v075/cache/usd/test/display_color/object_color.usd'

import lxusd.scripts as usd_scripts

usd_fnc_exporter.GeometryDisplayColorExporter(
    option=dict(
        file_src=f_src,
        file_tgt=f_tgt,
        location='/master/hi',
        #
        color_seed=10
    )
).set_run()


