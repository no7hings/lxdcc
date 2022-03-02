# coding:utf-8
from .. import obj_configure, obj_abstract

from ..core_objects import _obj_stack, _obj_raw

from lxbasic.objects import _bsc_obj_raw


class ObjToken(obj_abstract.AbsObjToken):
    TYPE_PATHSEP = obj_configure.Type.PATHSEP
    OBJ_PATHSEP = obj_configure.Obj.PATHSEP
    #
    PORT_PATHSEP = obj_configure.Port.PATHSEP
    PORT_ASSIGN_PATHSEP = obj_configure.PortAssign.PATHSEP
    def __init__(self):
        super(ObjToken, self).__init__()


class Type(obj_abstract.AbsType):
    PATHSEP = obj_configure.Type.PATHSEP
    def __init__(self, category, name):
        super(Type, self).__init__(category, name)

    def _get_value_class_(self, type_name, is_array):
        if is_array:
            return _obj_raw.Array
        #
        if obj_configure.Type.get_is_color(type_name):
            return _obj_raw.Color
        elif obj_configure.Type.get_is_vector(type_name):
            return _obj_raw.Vector
        elif obj_configure.Type.get_is_matrix(type_name):
            return _obj_raw.Matrix
        return _obj_raw.Constant


class Category(obj_abstract.AbsCategory):
    PATHSEP = obj_configure.Category.PATHSEP
    #
    TYPE_CLASS = Type
    def __init__(self, universe, name):
        super(Category, self).__init__(universe, name)


class PortChannel(obj_abstract.AbsPortChannel):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = obj_configure.Port.PATHSEP
    def __init__(self, parent, name):
        super(PortChannel, self).__init__(parent, name)


class PortElement(obj_abstract.AbsPortElement):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = obj_configure.Port.PATHSEP
    #
    PORT_CHANNEL_STACK_CLASS = _obj_stack.PortChannelStack
    PORT_CHANNEL_CLASS = PortChannel
    def __init__(self, parent, index):
        super(PortElement, self).__init__(parent, index)


class Port(obj_abstract.AbsPort):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = obj_configure.Port.PATHSEP
    #
    PORT_ELEMENT_STACK_CLASS = _obj_stack.PortElementStack
    PORT_ELEMENT_CLASS = PortElement
    #
    PORT_CHANNEL_STACK_CLASS = _obj_stack.PortChannelStack
    PORT_CHANNEL_CLASS = PortChannel
    def __init__(self, node, type_, assign, name):
        super(Port, self).__init__(node, type_, assign, name)


class Properties(obj_abstract.AbsProperties):
    PATHSEP = obj_configure.Properties.PATHSEP
    def __init__(self, obj, raw):
        super(Properties, self).__init__(obj, raw)


class Attributes(obj_abstract.AbsProperties):
    PATHSEP = obj_configure.Properties.PATHSEP
    def __init__(self, obj, raw):
        super(Attributes, self).__init__(obj, raw)


class ObjDagPath(obj_abstract.AbsObjDagPath):
    def __init__(self, path):
        super(ObjDagPath, self).__init__(path)


class PortDagPath(obj_abstract.AbsPortDagPath):
    def __init__(self, path):
        super(PortDagPath, self).__init__(path)


class Obj(obj_abstract.AbsObj):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = obj_configure.Obj.PATHSEP
    # port/def
    PORT_CLASS = Port
    PORT_STACK_CLASS = _obj_stack.PrxPortStack
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    ATTRIBUTES_CLASS = Attributes
    def __init__(self, type_, path):
        super(Obj, self).__init__(type_, path)


class PortQuery(obj_abstract.AbsPortQuery):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = obj_configure.Port.PATHSEP
    def __init__(self, obj_type, raw_type, port_path, port_assign, raw):
        super(PortQuery, self).__init__(obj_type, raw_type, port_path, port_assign, raw)


class ObjType(obj_abstract.AbsObjType):
    OBJ_TOKEN = ObjToken
    # type/def
    PATHSEP = obj_configure.ObjType.PATHSEP
    # obj_type/def
    DCC_OBJ_CLASS = Obj
    # port_query/def
    PORT_QUERY_CLASS = PortQuery
    PORT_QUERY_STACK_CLASS = _obj_stack.PortQueryStack
    def __init__(self, category, name):
        super(ObjType, self).__init__(category, name)


class ObjCategory(obj_abstract.AbsObjCategory):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = obj_configure.ObjCategory.PATHSEP
    #
    TYPE_CLASS = ObjType
    #
    # port_query/def
    PORT_QUERY_CLASS = PortQuery
    PORT_QUERY_STACK_CLASS = _obj_stack.PortQueryStack
    def __init__(self, universe, name):
        super(ObjCategory, self).__init__(universe, name)


class ObjConnection(obj_abstract.AbsObjConnection):
    OBJ_TOKEN = ObjToken
    OBJ_PATHSEP = obj_configure.Obj.PATHSEP
    PORT_PATHSEP = obj_configure.Port.PATHSEP
    PORT_ASSIGN_PATHSEP = obj_configure.PortAssign.PATHSEP
    def __init__(self, universe, source_obj_path, source_port_path, target_obj_path, target_port_path):
        super(ObjConnection, self).__init__(
            universe,
            source_obj_path, source_port_path,
            target_obj_path, target_port_path
        )


class ObjBind(obj_abstract.AbsObjBind):
    def __init__(self, universe, obj):
        super(ObjBind, self).__init__(universe, obj)


class ObjUniverse(obj_abstract.AbsObjUniverse):
    ROOT = obj_configure.Obj.PATHSEP
    #
    CATEGORY_STACK_CLASS = _obj_stack.CategoryStack
    CATEGORY_CLASS = Category
    TYPE_STACK_CLASS = _obj_stack.TypeStack
    #
    OBJ_CATEGORY_STACK_CLASS = _obj_stack.ObjCategoryStack
    OBJ_CATEGORY_CLASS = ObjCategory
    OBJ_TYPE_STACK_CLASS = _obj_stack.ObjTypeStack
    #
    OBJ_STACK_CLASS = _obj_stack.ObjStack
    #
    OBJ_CONNECTION_STACK_CLASS = _obj_stack.ObjConnectionStack
    OBJ_CONNECTION_CLASS = ObjConnection
    #
    OBJ_BIND_STACK_CLASS = _obj_stack.ObjBindStack
    OBJ_BIND_CLASS = ObjBind
    def __init__(self):
        super(ObjUniverse, self).__init__()
