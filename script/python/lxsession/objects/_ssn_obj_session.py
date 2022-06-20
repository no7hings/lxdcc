# coding:utf-8
from lxsession.objects import ssn_obj_abs

from lxsession.objects import _ssn_obj_executor


class OptionGuiSession(ssn_obj_abs.AbsSsnOptionGui):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(OptionGuiSession, self).__init__(*args, **kwargs)


class GuiSession(ssn_obj_abs.AbsSsnGui):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(GuiSession, self).__init__(*args, **kwargs)


class OptionActionSession(ssn_obj_abs.AbsSsnOptionAction):
    def __init__(self, *args, **kwargs):
        super(OptionActionSession, self).__init__(*args, **kwargs)


class OptionLauncherSession(ssn_obj_abs.AbsSsnOptionLauncher):
    def __init__(self, *args, **kwargs):
        super(OptionLauncherSession, self).__init__(*args, **kwargs)


class OptionToolPanelSession(ssn_obj_abs.AbsSsnOptionToolPanel):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(OptionToolPanelSession, self).__init__(*args, **kwargs)


class SsnOptionMethod(ssn_obj_abs.AbsSsnOptionMethod):
    EXECUTOR = _ssn_obj_executor.HookExecutor
    def __init__(self, *args, **kwargs):
        super(SsnOptionMethod, self).__init__(*args, **kwargs)


class RsvOptionHookMethodSession(ssn_obj_abs.AbsSsnRsvTaskOptionMethod):
    EXECUTOR = _ssn_obj_executor.RsvTaskHookExecutor
    def __init__(self, *args, **kwargs):
        super(RsvOptionHookMethodSession, self).__init__(*args, **kwargs)


class RsvObjActionSession(ssn_obj_abs.AbsSsnRsvObjAction):
    def __init__(self, *args, **kwargs):
        super(RsvObjActionSession, self).__init__(*args, **kwargs)


class RsvUnitActionSession(ssn_obj_abs.AbsSsnRsvUnitAction):
    def __init__(self, *args, **kwargs):
        super(RsvUnitActionSession, self).__init__(*args, **kwargs)


class ApplicationSession(ssn_obj_abs.AbsApplicationSession):
    def __init__(self, *args, **kwargs):
        super(ApplicationSession, self).__init__(*args, **kwargs)
