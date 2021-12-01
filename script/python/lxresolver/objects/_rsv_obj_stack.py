# coding:utf-8
from lxobj import obj_abstract


# <stack-project>
class ProjectStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(ProjectStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# <stack-task>
class EntityStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(EntityStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# <stack-task>
class TaskStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(TaskStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()
