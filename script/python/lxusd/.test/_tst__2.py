# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.set_environs_setup()

import lxusd.fnc.exporters as usd_fnc_exporter

f_src = '/l/temp/temporary/usd-export/2022_0913-dongchangbao/RI5BPR.usd'

f_tgt = '/l/prod/cgm/publish/shots/x30/x30250/cfx/cloth/x30250.cfx.cloth.v003/cache/nn_4y/usd/nn_4y.usda'

import lxusd.scripts as usd_scripts

usd_fnc_exporter.GeometryDisplayColorExporter(
    option=dict(

    )
).set_run()

