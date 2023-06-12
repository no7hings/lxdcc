# coding:utf-8
# noinspection PyUnresolvedReferences
import arnold as ai

import lxuniverse.objects as unv_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects
#
from lxarnold.dcc import and_obj_abstract


class Scene(and_obj_abstract.AbsObjScene):
    AR_OBJ_CATEGORY_MASK = [
        ai.AI_NODE_SHAPE,
        ai.AI_NODE_SHADER,
    ]
    #
    FILE_CLS = utl_dcc_objects.OsFile
    UNIVERSE_CLS = unv_objects.ObjUniverse
    def __init__(self, option=None):
        super(Scene, self).__init__(option=option)
