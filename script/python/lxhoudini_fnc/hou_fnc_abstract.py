# coding:utf-8
from lxutil import utl_core

from lxutil_fnc import utl_fnc_core, utl_fnc_abstract

from lxhoudini_fnc import hou_fnc_core


class AbsHouIspOp(utl_fnc_abstract.AbsChecker):
    FNC_CHECKER_LOADER_CLASS = hou_fnc_core.CheckerLoader
    FNC_ISP_IGNORE_CLASS = utl_fnc_core.IspIgnore
    def __init__(self, fnc_isp_path):
        super(AbsHouIspOp, self).__init__(fnc_isp_path)

    def set_check_run(self):
        raise NotImplementedError()
