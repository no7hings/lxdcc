# coding:utf-8
from lxutil_fnc import utl_fnc_core, utl_fnc_abstract

from . import stg_fnc_core


class AbsStgIsp(utl_fnc_abstract.AbsChecker):
    FNC_ISP_IGNORE_CLASS = utl_fnc_core.IspIgnore

    FNC_CHECKER_LOADER_CLASS = stg_fnc_core.CheckerLoader
    def __init__(self, fnc_isp_path):
        super(AbsStgIsp, self).__init__(fnc_isp_path)

    def set_check_run(self):
        raise NotImplementedError()
