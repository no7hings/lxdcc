# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs


class FncDccMeshMatcher(utl_fnc_obj_abs.AbsFncDccMeshMatcher):
    FNC_DCC_MESH_CLS = None
    def __init__(self, *args, **kwargs):
        super(FncDccMeshMatcher, self).__init__(*args, **kwargs)


class FncGeometryComparer(utl_fnc_obj_abs.AbsFncDccGeometryComparer):
    DCC_SCENE_CLS = None
    DCC_SCENE_OPT_CLS = None
    #
    FNC_DCC_MESH_MATCHER_CLS = FncDccMeshMatcher
    FNC_USD_MESH_REPAIRER_CLS = None
    #
    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    def __init__(self, *args, **kwargs):
        super(FncGeometryComparer, self).__init__(*args, **kwargs)

    def update_target_fnc(self):
        pass
