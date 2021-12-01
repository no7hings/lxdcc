# coding:utf-8
from lxdeadline.methods import ddl_mtd_abstract


class DdlMethodRunner(ddl_mtd_abstract.AbsDdlMethodRunner):
    def __init__(self, method_option, script_option, job_dependencies=None):
        super(DdlMethodRunner, self).__init__(method_option, script_option, job_dependencies)


class DdlRsvTaskMethodRunner(ddl_mtd_abstract.AbsDdlRsvTaskMethodRunner):
    def __init__(self, method_option, script_option, job_dependencies=None):
        super(DdlRsvTaskMethodRunner, self).__init__(method_option, script_option, job_dependencies)


class DdlRsvTaskRender(ddl_mtd_abstract.AbsDdlRsvTaskRender):
    def __init__(self, method_option, script_option, job_dependencies=None):
        super(DdlRsvTaskRender, self).__init__(method_option, script_option, job_dependencies)
