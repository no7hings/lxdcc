# coding:utf-8
# noinspection PyUnresolvedReferences
import arnold as ai

import lxobj.core_objects as core_dcc_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects
#
from lxarnold.dcc import and_obj_abstract


class Scene(and_obj_abstract.AbsObjScene):
    AR_OBJ_CATEGORY_MASK = [
        ai.AI_NODE_SHAPE,
        ai.AI_NODE_SHADER,
    ]
    #
    FILE_CLASS = utl_dcc_objects.OsFile
    UNIVERSE_CLASS = core_dcc_objects.ObjUniverse
    def __init__(self, option=None):
        super(Scene, self).__init__(option=option)
