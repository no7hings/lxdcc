# coding:utf-8
from LxData.datObjects import _datObjRaw, _datObjPath

from LxGraphic import grhCfg

from LxGraphic.grhObjects import _grhObjStack

from .. import ar_mtx_abstract

from ..ar_mtx_obectjs import _ar_mtx_obj_raw, _ar_mtx_obj_query, _ar_mtx_obj_port


class Node(ar_mtx_abstract.AbsDccObj):
    CLS_grh__cache_obj__variant = _datObjRaw.ObjVariant
    CLS_grh__cache_obj__variant_obj_stack = _grhObjStack.VariantObjStack

    CLS_grh__obj__obj_proxy_stack = _grhObjStack.ObjProxyStack

    CLS_grh__obj__path = _ar_mtx_obj_raw.Nodepath

    CLS_grh__obj__loader = _ar_mtx_obj_query.ObjLoader

    CLS_grh__node__typepath = _datObjPath.Typepath
    CLS_grh__node__datatype = _datObjRaw.Datatype

    CLS_grh__node__port_stack = _grhObjStack.PrxPortStack

    CLS_grh__node__connector = _ar_mtx_obj_port.Connector

    IST_grh__obj__query_builder = _ar_mtx_obj_query.GRH_OBJ_QUERY_BUILDER
    IST_grh__obj__queue = _ar_mtx_obj_query.GRH_OBJ_QUEUE

    VAR_grh__node__port_cls_dict = {
        grhCfg.GrhPortAssignQuery.gnport: _ar_mtx_obj_port.Gnport,
        grhCfg.GrhPortAssignQuery.gnport_channel: _ar_mtx_obj_port.Gnport,
        grhCfg.GrhPortAssignQuery.inport: _ar_mtx_obj_port.Inport,
        grhCfg.GrhPortAssignQuery.inport_channel: _ar_mtx_obj_port.Inport,
        grhCfg.GrhPortAssignQuery.otport: _ar_mtx_obj_port.Otport,
        grhCfg.GrhPortAssignQuery.otport_channel: _ar_mtx_obj_port.Otport,

        grhCfg.GrhPortAssignQuery.asport: _ar_mtx_obj_port.Asport,

        grhCfg.GrhPortAssignQuery.property: _ar_mtx_obj_port.Inport,
        grhCfg.GrhPortAssignQuery.visibility: _ar_mtx_obj_port.Inport
    }

    def __init__(self, *args, **kwargs):
        self._initAbsDccNode(*args, **kwargs)
