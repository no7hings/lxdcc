# coding:utf-8
import lxsession.abstracts as ssn_abstracts

from lxsession.objects import _ssn_obj_executor


class OptionGuiSession(ssn_abstracts.AbsSsnOptionGui):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(OptionGuiSession, self).__init__(*args, **kwargs)


class GuiSession(ssn_abstracts.AbsSsnGui):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(GuiSession, self).__init__(*args, **kwargs)


class ToolSession(ssn_abstracts.AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(ToolSession, self).__init__(*args, **kwargs)



class OptionActionSession(ssn_abstracts.AbsSsnOptionAction):
    def __init__(self, *args, **kwargs):
        super(OptionActionSession, self).__init__(*args, **kwargs)


class DatabaseOptionActionSession(ssn_abstracts.AbsSsnDatabaseOptionAction):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(DatabaseOptionActionSession, self).__init__(*args, **kwargs)


class OptionLauncherSession(ssn_abstracts.AbsSsnOptionLauncher):
    def __init__(self, *args, **kwargs):
        super(OptionLauncherSession, self).__init__(*args, **kwargs)


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


class RsvObjActionSession(ssn_abstracts.AbsSsnRsvObjAction):
    def __init__(self, *args, **kwargs):
        super(RsvObjActionSession, self).__init__(*args, **kwargs)


class RsvUnitActionSession(ssn_abstracts.AbsSsnRsvUnitAction):
    def __init__(self, *args, **kwargs):
        super(RsvUnitActionSession, self).__init__(*args, **kwargs)


class ApplicationSession(ssn_abstracts.AbsApplicationSession):
    def __init__(self, *args, **kwargs):
        super(ApplicationSession, self).__init__(*args, **kwargs)
