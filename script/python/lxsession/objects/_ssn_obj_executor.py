# coding:utf-8
from lxsession.objects import ssn_obj_ect_abs


class HookExecutor(ssn_obj_ect_abs.AbsHookExecutor):
    def __init__(self, *args, **kwargs):
        super(HookExecutor, self).__init__(*args, **kwargs)


class RsvTaskHookExecutor(ssn_obj_ect_abs.AbsRsvTaskHookExecutor):
    def __init__(self, *args, **kwargs):
        super(RsvTaskHookExecutor, self).__init__(*args, **kwargs)
