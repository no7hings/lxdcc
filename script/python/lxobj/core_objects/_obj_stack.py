# coding:utf-8
from .. import obj_abstract


# category
class CategoryStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(CategoryStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# type
class TypeStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(TypeStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# port channel
class PortChannelStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PortChannelStack, self).__init__()

    def get_key(self, obj):
        return obj.name


# port element
class PortElementStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PortElementStack, self).__init__()

    def get_key(self, obj):
        return obj.index


class PortQueryStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PortQueryStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# port
class PortStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PortStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# connection
class ObjConnectionStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(ObjConnectionStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


class ObjBindStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(ObjBindStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# node type
class ObjCategoryStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(ObjCategoryStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# type
class ObjTypeStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(ObjTypeStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# obj
class ObjStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(ObjStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()
