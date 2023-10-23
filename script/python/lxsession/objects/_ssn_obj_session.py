# coding:utf-8
import lxsession.abstracts as ssn_abstracts

from lxsession.objects import _ssn_obj_executor


class OptionGuiSession(ssn_abstracts.AbsSsnOptionGui):
    EXECUTOR = _ssn_obj_executor.HookExecutor

    def __init__(self, *args, **kwargs):
        super(OptionGuiSession, self).__init__(*args, **kwargs)


class DatabaseOptionActionSession(ssn_abstracts.AbsSsnDatabaseOptionAction):
    EXECUTOR = _ssn_obj_executor.HookExecutor

    def __init__(self, *args, **kwargs):
        super(DatabaseOptionActionSession, self).__init__(*args, **kwargs)


class OptionToolPanelSession(ssn_abstracts.AbsSsnOptionToolPanel):
    EXECUTOR = _ssn_obj_executor.HookExecutor

    def __init__(self, *args, **kwargs):
        super(OptionToolPanelSession, self).__init__(*args, **kwargs)


class RsvOptionToolPanelSession(ssn_abstracts.AbsSsnRsvOptionToolPanel):
    EXECUTOR = _ssn_obj_executor.HookExecutor

    def __init__(self, *args, **kwargs):
        super(RsvOptionToolPanelSession, self).__init__(*args, **kwargs)


class SsnOptionMethod(ssn_abstracts.AbsSsnOptionMethod):
    EXECUTOR = _ssn_obj_executor.HookExecutor

    def __init__(self, *args, **kwargs):
        super(SsnOptionMethod, self).__init__(*args, **kwargs)


class RsvProjectMethodSession(ssn_abstracts.AbsSsnRsvProjectOptionMethod):
    EXECUTOR = _ssn_obj_executor.RsvProjectHookExecutor

    def __init__(self, *args, **kwargs):
        super(RsvProjectMethodSession, self).__init__(*args, **kwargs)


class RsvTaskMethodSession(ssn_abstracts.AbsSsnRsvTaskOptionMethod):
    EXECUTOR = _ssn_obj_executor.RsvTaskHookExecutor

    def __init__(self, *args, **kwargs):
        super(RsvTaskMethodSession, self).__init__(*args, **kwargs)


class RsvActionSession(ssn_abstracts.AbsSsnRsvAction):
    def __init__(self, *args, **kwargs):
        super(RsvActionSession, self).__init__(*args, **kwargs)


class RsvUnitActionSession(ssn_abstracts.AbsSsnRsvUnitAction):
    def __init__(self, *args, **kwargs):
        super(RsvUnitActionSession, self).__init__(*args, **kwargs)
