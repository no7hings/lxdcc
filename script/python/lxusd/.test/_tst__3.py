# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.set_environs_setup()

import lxusd.fnc.exporters as usd_fnc_exporter

f = '/data/f/usd_uv_map_export_test_0/test_0.usda'

from lxusd import usd_core

s_opt = usd_core.UsdStageOpt(f)

p = s_opt.get_obj('/pPlane1/pPlaneShape1')

print p

m = usd_core.UsdGeom.Mesh(p)

print usd_core.UsdMeshOpt(
    m
).get_display_color_map_from_uv_map('st')


