# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.build_environ()

from lxusd import usd_core

f_src = '/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/nn_4y.srf.surfacing.v075/cache/usd/nn_4y.usda'

f_tgt = '/l/prod/cgm/publish/shots/x30/x30270/cfx/cloth/x30270.cfx.cloth.v002/cache/nn_4y/usd/nn_4y.usda'

import lxusd.scripts as usd_scripts

usd_scripts.UsdMeshSubdiv(
    f_src, f_tgt
).set_run()
