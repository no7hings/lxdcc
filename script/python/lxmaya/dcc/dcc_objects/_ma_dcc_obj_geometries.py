# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from .. import mya_dcc_obj_abs

from ...dcc.dcc_objects import _ma_dcc_obj_geometry


class Meshes(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = [
        'mesh',
    ]
    #
    DCC_OBJ_CLASS = _ma_dcc_obj_geometry.Mesh
    def __init__(self, *args):
        super(Meshes, self).__init__(*args)
