# coding:utf-8
import os
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom, Gf, Ar

from lxbasic import bsc_core

from lxusd import usd_setup

usd_setup.UsdSetup.set_environs_setup()

from lxusd import usd_core

usdFilePath = '/l/prod/cgm/work/assets/vfx/efx_dissipation_grandma/srf/surfacing/katana/set/x40130/v012/x40130.usda'

stage = Usd.Stage.Open(usdFilePath, Usd.Stage.LoadAll)

stage_opt = usd_core.UsdStageOpt(
    stage
)

p = stage_opt.get_obj(
    '/assets/efx/efx_dissipation_grandma'
)

prim_opt = usd_core.UsdPrimOpt(
    p
)

for i in prim_opt.get_children():
    i_opt = usd_core.UsdPrimOpt(i)
    i_port = i_opt.get_port('userProperties:pgOpIn:usd:opArgs:fileName')
    i_file_path = i_port.Get().resolvedPath

    i_file_path_ = bsc_core.MultiplyFileNameMtd.set_convert_to(
        i_file_path, ['*.####.{ext}']
    )
    print i_file_path_

    # i_stage_opt = usd_core.UsdStageOpt(i_file_path)
    # sub_paths = i_stage_opt.get_all_obj_paths()


