# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs


class FncDccMeshMatcher(utl_fnc_obj_abs.AbsFncDccMeshMatcher):
    FNC_DCC_MESH_CLASS = None
    def __init__(self, *args, **kwargs):
        super(FncDccMeshMatcher, self).__init__(*args, **kwargs)


class FncGeometryComparer(utl_fnc_obj_abs.AbsUsdGeometryComparer):
    FNC_DCC_MESH_MATCHER_CLASS = FncDccMeshMatcher
    def __init__(self, *args, **kwargs):
        super(FncGeometryComparer, self).__init__(*args, **kwargs)
