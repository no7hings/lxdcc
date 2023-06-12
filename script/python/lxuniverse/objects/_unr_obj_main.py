# coding:utf-8
from lxbasic.objects import _bsc_obj_raw

from lxuniverse import unr_configure

import lxuniverse.abstracts as unr_abstracts

from lxuniverse.objects import _unr_obj_stack, _unr_obj_raw


class ObjToken(unr_abstracts.AbsObjToken):
    TYPE_PATHSEP = unr_configure.Type.PATHSEP
    OBJ_PATHSEP = unr_configure.Obj.PATHSEP
    #
    PORT_PATHSEP = unr_configure.Port.PATHSEP
    PORT_ASSIGN_PATHSEP = unr_configure.PortAssign.PATHSEP
    def __init__(self):
        super(ObjToken, self).__init__()


class Type(unr_abstracts.AbsType):
    PATHSEP = unr_configure.Type.PATHSEP
    def __init__(self, category, name):
        super(Type, self).__init__(category, name)

    def _get_value_class_(self, type_name, is_array):
        if is_array:
            return _unr_obj_raw.Array
        #
        if unr_configure.Type.get_is_color(type_name):
            return _unr_obj_raw.Color
        elif unr_configure.Type.get_is_vector(type_name):
            return _unr_obj_raw.Vector
        elif unr_configure.Type.get_is_matrix(type_name):
            return _unr_obj_raw.Matrix
        return _unr_obj_raw.Constant


class Category(unr_abstracts.AbsCategory):
    PATHSEP = unr_configure.Category.PATHSEP
    #
    TYPE_CLS = Type
    def __init__(self, universe, name):
        super(Category, self).__init__(universe, name)


class PortChannel(unr_abstracts.AbsPortChannel):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_configure.Port.PATHSEP
    def __init__(self, parent, name):
        super(PortChannel, self).__init__(parent, name)


class PortElement(unr_abstracts.AbsPortElement):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_configure.Port.PATHSEP
    #
    PORT_CHANNEL_STACK_CLS = _unr_obj_stack.PortChannelStack
    PORT_CHANNEL_CLS = PortChannel
    def __init__(self, parent, index):
        super(PortElement, self).__init__(parent, index)


class Port(unr_abstracts.AbsPort):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_configure.Port.PATHSEP
    #
    PORT_ELEMENT_STACK_CLS = _unr_obj_stack.PortElementStack
    PORT_ELEMENT_CLS = PortElement
    #
    PORT_CHANNEL_STACK_CLS = _unr_obj_stack.PortChannelStack
    PORT_CHANNEL_CLS = PortChannel
    def __init__(self, node, type_, assign, name):
        super(Port, self).__init__(node, type_, assign, name)


class Properties(unr_abstracts.AbsProperties):
    PATHSEP = unr_configure.Properties.PATHSEP
    def __init__(self, obj, raw):
        super(Properties, self).__init__(obj, raw)


class Attributes(unr_abstracts.AbsProperties):
    PATHSEP = unr_configure.Properties.PATHSEP
    def __init__(self, obj, raw):
        super(Attributes, self).__init__(obj, raw)


class ObjDagPath(unr_abstracts.AbsObjDagPath):
    def __init__(self, path):
        super(ObjDagPath, self).__init__(path)


class PortDagPath(unr_abstracts.AbsPortDagPath):
    def __init__(self, path):
        super(PortDagPath, self).__init__(path)


class Obj(unr_abstracts.AbsObj):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_configure.Obj.PATHSEP
    # port/def
    PORT_CLS = Port
    PORT_STACK_CLS = _unr_obj_stack.PrxPortStack
    #
    PROPERTIES_CLS = _bsc_obj_raw.Properties
    ATTRIBUTES_CLS = Attributes
    def __init__(self, type_, path):
        super(Obj, self).__init__(type_, path)


class PortQuery(unr_abstracts.AbsPortQuery):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_configure.Port.PATHSEP
    def __init__(self, obj_type, raw_type, port_path, port_assign, raw):
        super(PortQuery, self).__init__(obj_type, raw_type, port_path, port_assign, raw)


class ObjType(unr_abstracts.AbsObjType):
    OBJ_TOKEN = ObjToken
    # type/def
    PATHSEP = unr_configure.ObjType.PATHSEP
    # obj_type/def
    DCC_NODE_CLS = Obj
    # port_query/def
    PORT_QUERY_CLS = PortQuery
    PORT_QUERY_STACK_CLS = _unr_obj_stack.PortQueryStack
    def __init__(self, category, name):
        super(ObjType, self).__init__(category, name)


class ObjCategory(unr_abstracts.AbsObjCategory):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_configure.ObjCategory.PATHSEP
    #
    TYPE_CLS = ObjType
    #
    # port_query/def
    PORT_QUERY_CLS = PortQuery
    PORT_QUERY_STACK_CLS = _unr_obj_stack.PortQueryStack
    def __init__(self, universe, name):
        super(ObjCategory, self).__init__(universe, name)


class ObjConnection(unr_abstracts.AbsObjConnection):
    OBJ_TOKEN = ObjToken
    OBJ_PATHSEP = unr_configure.Obj.PATHSEP
    PORT_PATHSEP = unr_configure.Port.PATHSEP
    PORT_ASSIGN_PATHSEP = unr_configure.PortAssign.PATHSEP
    def __init__(self, universe, source_obj_path, source_port_path, target_obj_path, target_port_path):
        super(ObjConnection, self).__init__(
            universe,
            source_obj_path, source_port_path,
            target_obj_path, target_port_path
        )


class ObjBind(unr_abstracts.AbsObjBind):
    def __init__(self, universe, obj):
        super(ObjBind, self).__init__(universe, obj)


class ObjUniverse(unr_abstracts.AbsObjUniverse):
    ROOT = unr_configure.Obj.PATHSEP
    #
    CATEGORY_STACK_CLS = _unr_obj_stack.CategoryStack
    CATEGORY_CLS = Category
    TYPE_STACK_CLS = _unr_obj_stack.TypeStack
    #
    OBJ_CATEGORY_STACK_CLS = _unr_obj_stack.ObjCategoryStack
    OBJ_CATEGORY_CLS = ObjCategory
    OBJ_TYPE_STACK_CLS = _unr_obj_stack.ObjTypeStack
    #
    OBJ_STACK_CLS = _unr_obj_stack.ObjStack
    OBJ_STACK_CLS_TEST = _unr_obj_stack.ObjStackTest
    #
    OBJ_CONNECTION_STACK_CLS = _unr_obj_stack.ObjConnectionStack
    OBJ_CONNECTION_CLS = ObjConnection
    #
    OBJ_BIND_STACK_CLS = _unr_obj_stack.ObjBindStack
    OBJ_BIND_CLS = ObjBind
    def __init__(self):
        super(ObjUniverse, self).__init__()
