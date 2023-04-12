# coding:utf-8
import lxsession.abstracts as ssn_abstracts

import lxdeadline.objects as ddl_objects


class HookExecutor(ssn_abstracts.AbsHookExecutor):
    SUBMITTER_CLASS = ddl_objects.DdlSubmiter
    def __init__(self, *args, **kwargs):
        super(HookExecutor, self).__init__(*args, **kwargs)


class RsvProjectHookExecutor(ssn_abstracts.AbsRsvProjectMethodHookExecutor):
    SUBMITTER_CLASS = ddl_objects.DdlRsvProjectSubmiter
    def __init__(self, *args, **kwargs):
        super(RsvProjectHookExecutor, self).__init__(*args, **kwargs)


class RsvTaskHookExecutor(ssn_abstracts.AbsRsvTaskMethodHookExecutor):
    SUBMITTER_CLASS = ddl_objects.DdlRsvTaskSubmiter
    def __init__(self, *args, **kwargs):
        super(RsvTaskHookExecutor, self).__init__(*args, **kwargs)
