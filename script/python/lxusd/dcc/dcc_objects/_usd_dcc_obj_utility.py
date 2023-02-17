# coding:utf-8
import lxuniverse.objects as unv_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects
#
from lxusd.dcc import usd_dcc_obj_abstract


class Scene(usd_dcc_obj_abstract.AbsUsdObjScene):
    FILE_CLASS = utl_dcc_objects.OsFile
    UNIVERSE_CLASS = unv_objects.ObjUniverse
    def __init__(self):
        super(Scene, self).__init__()
