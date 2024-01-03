# coding:utf-8
import lxsession.abstracts as ssn_abstracts

import lxbasic.deadline.core as bsc_ddl_core


class HookExecutor(ssn_abstracts.AbsHookExecutor):
    SUBMITTER_CLS = bsc_ddl_core.DdlSubmiter

    def __init__(self, *args, **kwargs):
        super(HookExecutor, self).__init__(*args, **kwargs)


class RsvProjectHookExecutor(ssn_abstracts.AbsRsvProjectMethodHookExecutor):
    SUBMITTER_CLS = bsc_ddl_core.DdlSubmiterForRsvProject

    def __init__(self, *args, **kwargs):
        super(RsvProjectHookExecutor, self).__init__(*args, **kwargs)


class RsvTaskHookExecutor(ssn_abstracts.AbsRsvTaskMethodHookExecutor):
    SUBMITTER_CLS = bsc_ddl_core.DdlSubmiterForRsvTask

    def __init__(self, *args, **kwargs):
        super(RsvTaskHookExecutor, self).__init__(*args, **kwargs)
