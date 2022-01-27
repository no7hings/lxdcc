# coding:utf-8
from lxdeadline.methods import ddl_mtd_abstract


class HookExecutor(ddl_mtd_abstract.AbsHookExecutor):
    def __init__(self, method_option, script_option, job_dependencies=None):
        super(HookExecutor, self).__init__(method_option, script_option, job_dependencies)


class RsvTaskHookExecutor(ddl_mtd_abstract.AbsRsvTaskHookExecutor):
    def __init__(self, method_option, script_option, job_dependencies=None):
        super(RsvTaskHookExecutor, self).__init__(method_option, script_option, job_dependencies)


class DdlRsvTaskRender(ddl_mtd_abstract.AbsDdlRsvTaskRender):
    def __init__(self, method_option, script_option, job_dependencies=None):
        super(DdlRsvTaskRender, self).__init__(method_option, script_option, job_dependencies)
