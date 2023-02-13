# coding:utf-8
from lxutil_fnc import utl_fnc_core, utl_fnc_abstract

from . import ma_fnc_core


class AbsMyaChecker(utl_fnc_abstract.AbsChecker):
    # loader method
    FNC_CHECKER_LOADER_CLASS = ma_fnc_core.CheckerLoader
    # ignore method
    FNC_ISP_IGNORE_CLASS = utl_fnc_core.IspIgnore
    def __init__(self, fnc_isp_path):
        super(AbsMyaChecker, self).__init__(fnc_isp_path)

    def set_check_run(self):
        raise NotImplementedError()


class AbsMyaTaskExporter(utl_fnc_abstract.AbsTaskExporter):
    METHOD_CONFIGURE_CLASS = ma_fnc_core.ExporterConfigure
    def __init__(self, key, task_properties):
        super(AbsMyaTaskExporter, self).__init__(key, task_properties)

    def set_export_run(self):
        raise NotImplementedError()
