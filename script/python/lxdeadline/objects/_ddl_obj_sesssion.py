# coding:utf-8
from ._ddl_obj_utility import *


class DdlSubmiter(ddl_obj_abs.AbsDdlSubmiter):
    CON = CON
    CONFIGURE_FILE_PATH = bsc_core.RscConfigure.get_yaml('session/deadline/submiter')

    def __init__(self, *args, **kwargs):
        super(DdlSubmiter, self).__init__(*args, **kwargs)


class DdlRsvProjectSubmiter(ddl_obj_abs.AbsDdlSubmiter):
    CON = CON
    CONFIGURE_FILE_PATH = bsc_core.RscConfigure.get_yaml('session/deadline/rsv-project-submiter')

    def __init__(self, *args, **kwargs):
        super(DdlRsvProjectSubmiter, self).__init__(*args, **kwargs)


class DdlRsvTaskSubmiter(ddl_obj_abs.AbsDdlSubmiter):
    CON = CON
    CONFIGURE_FILE_PATH = bsc_core.RscConfigure.get_yaml('session/deadline/rsv-task-submiter')

    def __init__(self, *args, **kwargs):
        super(DdlRsvTaskSubmiter, self).__init__(*args, **kwargs)
