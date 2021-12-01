# coding:utf-8
from .. import usdObjAbs


class ObjSceneLoader(usdObjAbs.AbsUsdObjSceneLoader):
    def __init__(self, *args, **kwargs):
        self._initAbsDccObjScene(*args, **kwargs)


GRH_OBJ_SCENE_LOADER = ObjSceneLoader()
