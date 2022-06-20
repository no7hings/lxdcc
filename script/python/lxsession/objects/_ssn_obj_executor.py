# coding:utf-8
from lxsession.objects import ssn_obj_ect_abs

import lxdeadline.objects as ddl_objects


class HookExecutor(ssn_obj_ect_abs.AbsHookExecutor):
    SUBMITTER_CLASS = ddl_objects.DdlSubmiter
    def __init__(self, *args, **kwargs):
        super(HookExecutor, self).__init__(*args, **kwargs)


class RsvTaskHookExecutor(ssn_obj_ect_abs.AbsRsvTaskMethodHookExecutor):
    SUBMITTER_CLASS = ddl_objects.DdlRsvTaskSubmiter
    def __init__(self, *args, **kwargs):
        super(RsvTaskHookExecutor, self).__init__(*args, **kwargs)
