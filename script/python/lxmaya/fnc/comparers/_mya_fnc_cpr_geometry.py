# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs

from lxmaya.fnc import mya_fnc_obj_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators


class FncDccMeshMatcher(utl_fnc_obj_abs.AbsFncDccMeshMatcher):
    FNC_DCC_MESH_CLASS = mya_fnc_obj_core.FncDccMesh
    def __init__(self, *args, **kwargs):
        super(FncDccMeshMatcher, self).__init__(*args, **kwargs)


class FncUsdMeshRepairer(utl_fnc_obj_abs.AbsFncUsdMeshRepairer):
    FNC_USD_MESH_CLASS = mya_fnc_obj_core.FncUsdMesh
    def __init__(self, *args, **kwargs):
        super(FncUsdMeshRepairer, self).__init__(*args, **kwargs)


class FncGeometryComparer(utl_fnc_obj_abs.AbsFncDccGeometryComparer):
    DCC_SCENE_CLASS = mya_dcc_objects.Scene
    DCC_SCENE_OPT_CLASS = mya_dcc_operators.SceneOpt
    #
    FNC_DCC_MESH_MATCHER_CLASS = FncDccMeshMatcher
    FNC_USD_MESH_REPAIRER_CLASS = FncUsdMeshRepairer
    #
    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    DCC_NAMESPACE = 'maya'
    def __init__(self, *args, **kwargs):
        super(FncGeometryComparer, self).__init__(*args, **kwargs)
