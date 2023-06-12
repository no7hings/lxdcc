# coding:utf-8
import lxbasic.objects as bsc_objects

import lxuniverse.objects as unv_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_fnc.dcc import utl_fnc_dcc_abstract


class Scene(utl_fnc_dcc_abstract.AbsObjScene):
    FILE_CLS = utl_dcc_objects.OsFile
    UNIVERSE_CLS = unv_objects.ObjUniverse
    #
    CONFIGURE_CLS = bsc_objects.Configure
    def __init__(self):
        super(Scene, self).__init__()
