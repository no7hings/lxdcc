# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.set_environs_setup()

from lxusd import usd_core

f_src = '/l/temp/temporary/usd-export/2022_0913-dongchangbao/RI5BPR.usd'

f_tgt = '/l/prod/cgm/publish/shots/x30/x30250/cfx/cloth/x30250.cfx.cloth.v003/cache/nn_4y/usd/nn_4y.usda'

import lxusd.scripts as usd_scripts

usd_scripts.UsdMeshCompare(
    f_src,
    f_tgt
).test()


