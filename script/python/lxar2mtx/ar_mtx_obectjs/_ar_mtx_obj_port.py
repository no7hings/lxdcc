# coding:utf-8
from LxData.datObjects import _datObjRaw

from LxGraphic.grhObjects import _grhObjStack

from .. import ar_mtx_abstract

from ..ar_mtx_obectjs import _ar_mtx_obj_raw, _ar_mtx_obj_query


class Connector(ar_mtx_abstract.AbsDccConnector):
    def __init__(self, *args):
        self._initAbsDccConnector(*args)


class Gnport(ar_mtx_abstract.AbsDccPort):
    CLS_grh__cache_obj__variant = _datObjRaw.ObjVariant
    CLS_grh__cache_obj__variant_obj_stack = _grhObjStack.VariantObjStack

    CLS_grh__obj__obj_stack = _grhObjStack.ObjStack
    CLS_grh__obj__obj_proxy_stack = _grhObjStack.ObjProxyStack
    CLS_grh__obj__path = _ar_mtx_obj_raw.Attrpath

    CLS_grh__port__porttype = _datObjRaw.Porttype
    CLS_grh__port__datatype = _datObjRaw.Datatype
    CLS_grh__port__assign = _datObjRaw.Name

    CLS_grh__obj__loader = _ar_mtx_obj_query.ObjLoader
    IST_grh__obj__query_builder = _ar_mtx_obj_query.GRH_OBJ_QUERY_BUILDER
    IST_grh__obj__queue = _ar_mtx_obj_query.GRH_OBJ_QUEUE

    def __init__(self, *args):
        self._initAbsDccPort(*args)


class Inport(ar_mtx_abstract.AbsDccPort):
    CLS_grh__cache_obj__variant = _datObjRaw.ObjVariant
    CLS_grh__cache_obj__variant_obj_stack = _grhObjStack.VariantObjStack

    CLS_grh__obj__obj_stack = _grhObjStack.ObjStack
    CLS_grh__obj__obj_proxy_stack = _grhObjStack.ObjProxyStack
    CLS_grh__obj__path = _ar_mtx_obj_raw.Attrpath

    CLS_grh__port__porttype = _datObjRaw.Porttype
    CLS_grh__port__datatype = _datObjRaw.Datatype
    CLS_grh__port__assign = _datObjRaw.Name

    CLS_grh__obj__loader = _ar_mtx_obj_query.ObjLoader
    IST_grh__obj__query_builder = _ar_mtx_obj_query.GRH_OBJ_QUERY_BUILDER
    IST_grh__obj__queue = _ar_mtx_obj_query.GRH_OBJ_QUEUE

    def __init__(self, *args):
        self._initAbsDccPort(*args)


class Otport(ar_mtx_abstract.AbsDccPort):
    CLS_grh__cache_obj__variant = _datObjRaw.ObjVariant
    CLS_grh__cache_obj__variant_obj_stack = _grhObjStack.VariantObjStack

    CLS_grh__obj__obj_stack = _grhObjStack.ObjStack
    CLS_grh__obj__obj_proxy_stack = _grhObjStack.ObjProxyStack
    CLS_grh__obj__path = _ar_mtx_obj_raw.Attrpath

    CLS_grh__port__porttype = _datObjRaw.Porttype
    CLS_grh__port__datatype = _datObjRaw.Datatype
    CLS_grh__port__assign = _datObjRaw.Name

    CLS_grh__obj__loader = _ar_mtx_obj_query.ObjLoader
    IST_grh__obj__query_builder = _ar_mtx_obj_query.GRH_OBJ_QUERY_BUILDER
    IST_grh__obj__queue = _ar_mtx_obj_query.GRH_OBJ_QUEUE

    def __init__(self, *args):
        self._initAbsDccPort(*args)


class Asport(ar_mtx_abstract.AbsDccPort):
    CLS_grh__cache_obj__variant = _datObjRaw.ObjVariant
    CLS_grh__cache_obj__variant_obj_stack = _grhObjStack.VariantObjStack

    CLS_grh__obj__obj_stack = _grhObjStack.ObjStack
    CLS_grh__obj__obj_proxy_stack = _grhObjStack.ObjProxyStack
    CLS_grh__obj__path = _ar_mtx_obj_raw.Attrpath

    CLS_grh__port__porttype = _datObjRaw.Porttype
    CLS_grh__port__datatype = _datObjRaw.Datatype
    CLS_grh__port__assign = _datObjRaw.Name

    CLS_grh__obj__loader = _ar_mtx_obj_query.ObjLoader
    IST_grh__obj__query_builder = _ar_mtx_obj_query.GRH_OBJ_QUERY_BUILDER
    IST_grh__obj__queue = _ar_mtx_obj_query.GRH_OBJ_QUEUE

    def __init__(self, *args):
        self._initAbsDccPort(*args)


