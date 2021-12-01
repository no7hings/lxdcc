# coding:utf-8
from LxData import datObjAbs

from LxData.datObjects import _datObjRaw

from lxarnold import and_configure


class Objnamespace(datObjAbs.AbsDatObjNamespace):
    CLS_dat__obj_path__name = _datObjRaw.Name

    CLS_dat__obj_path__objsep = and_configure.Namespace.PATHSEP

    def __init__(self, *args):
        self._initAbsDatObjNamespace(*args)


class Objname(datObjAbs.AbsDatObjName):
    CLS_dat__obj_name__namespace = Objnamespace
    CLS_dat__obj_name__name = _datObjRaw.Name

    def __init__(self, *args):
        self._initAbsDatObjName(*args)


class Portpath(datObjAbs.AbsDatObjPath):
    CLS_dat__obj_path__name = _datObjRaw.ObjName

    CLS_dat__obj_path__objsep = and_configure.Port.PATHSEP

    def __init__(self, *args):
        self._initAbsDatObjPath(*args)


class Nodepath(datObjAbs.AbsDatObjPath):
    CLS_dat__obj_path__name = _datObjRaw.ObjName

    CLS_dat__obj_path__objsep = and_configure.Node.PATHSEP

    def __init__(self, *args):
        self._initAbsDatObjPath(*args)


class Attrpath(datObjAbs.AbsDatObjComppath):
    CLS_dat__comppath__nodepath = Nodepath
    CLS_dat__comppath__portpath = Portpath

    def __init__(self, *args):
        self._initAbsDatObjComppath(*args)
