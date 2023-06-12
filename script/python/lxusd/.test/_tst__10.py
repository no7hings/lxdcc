# coding:utf-8
import os
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom, Gf, Ar

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.build_environ()

from lxusd import usd_core

j_stage_opt = usd_core.UsdStageOpt(
    '/l/prod/cgm/publish/shots/x40/x40130/efx/efx_dissipation_grandma/x40130.efx.efx_dissipation_grandma.v008/cache/release_grandma/usd/release_grandma.1001.usd'
)

print j_stage_opt.get_all_obj_paths()
