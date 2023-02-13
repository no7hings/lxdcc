# coding:utf-8
from lxutil_fnc import utl_fnc_abstract

from . import hou_fnc_configure


class CheckerCreator(utl_fnc_abstract.AbsTaskMethodCreator):
    METHODS_CONFIGURE = hou_fnc_configure.Scheme.CHECKER_CONFIGURES
    #
    APPLICATION_NAME = 'houdini'
    METHOD_MODULE_PATH = 'lxhoudini_fnc.checker'
    def __init__(self, fnc_scn_isp_paths):
        super(CheckerCreator, self).__init__(fnc_scn_isp_paths)


class CheckerLoader(utl_fnc_abstract.AbsCheckerLoader):
    METHODS_CONFIGURE = hou_fnc_configure.Scheme.CHECKER_CONFIGURES
    def __init__(self, *args):
        super(CheckerLoader, self).__init__(*args)


class StpLoader(utl_fnc_abstract.AbsStpLoader):
    STEPS_SCHEME = hou_fnc_configure.Scheme.STEPS
    def __init__(self, *args):
        super(StpLoader, self).__init__(*args)
