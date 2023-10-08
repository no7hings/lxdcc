# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs

import lxcontent.objects as ctt_objects

from lxutil import utl_configure


class TaskMethodsLoader(utl_fnc_obj_abs.AbsTaskMethodsLoader):
    CONFIGURE_CLS = ctt_objects.Configure
    METHODS_CONFIGURE_PATH = utl_configure.UtilityMethodData.get('main')

    def __init__(self, task_properties):
        super(TaskMethodsLoader, self).__init__(task_properties)
