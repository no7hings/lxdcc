# coding:utf-8
from LxData.datObjects import _datObjRaw
# graphic
from LxGraphic import grhCfg, grhObjAbs

from LxGraphic.grhObjects import _grhObjStack, _grhObjQuery
# materialx
from LxMtx import mtxCfg

from LxMtx.mtxObjects import _mtxObjQuery
# dcc
from .. import ar_mtx_configure

from ..ar_mtx_obectjs import _ar_mtx_obj_query
# dcc to materialx
from .. import ar2mtx_configure, ar2mtx_abstract


class TrsObjLoader(ar2mtx_abstract.AbsDcc2mtxTrsObjLoader):
    VAR_grh__trs_obj_loader__node_property_key_list = [
        grhCfg.GrhUtility.DEF_grh__keyword_port_setter,
        grhCfg.GrhUtility.DEF_grh__keyword__custom_node,
        grhCfg.GrhUtility.DEF_grh__keyword__create_expression,
        grhCfg.GrhUtility.DEF_grh__keyword__after_expression
    ]

    VAR_grh__trs_obj_loader__port_property_key_list = [
        grhCfg.GrhUtility.DEF_grh__keyword_portraw_converter,
        grhCfg.GrhUtility.DEF_grh__keyword_datatype_convert
    ]

    def __init__(self, *args):
        self._initAbsDcc2mtxTrsObjLoader(*args)


class TrsObjQueryrawCreator(ar2mtx_abstract.AbsDcc2mtxObjQueryrawCreator):
    CLS_grh__trs_obj_queryraw_creator__node_stack = _grhObjStack.TrsNodeQueryrawStack
    CLS_grh__trs_obj_queryraw_creator__node = _grhObjQuery.TrsNodeQueryraw

    CLS_grh__trs_obj_queryraw_creator__obj_loader = TrsObjLoader

    VAR_grh__trs_obj_queryraw_creator__node_file = ar2mtx_configure.DataFile.NODE
    VAR_grh__trs_obj_queryraw_creator__geometry_file = ar2mtx_configure.DataFile.GEOMETRY
    VAR_grh__trs_obj_queryraw_creator__material_file = ar2mtx_configure.DataFile.MATERIAL

    IST_grh__trs_obj_queryraw_creator__source = _ar_mtx_obj_query.GRH_OBJ_QUERYRAW_CREATOR
    IST_grh__trs_obj_queryraw_creator__target = _mtxObjQuery.GRH_OBJ_QUERYRAW_CREATOR

    def __init__(self, *args):
        self._initAbsDcc2mtxObjQueryrawCreator(*args)


GRH_TRS_OBJ_QUERYRAW_CREATOR = TrsObjQueryrawCreator()


class TrsPortQuery(grhObjAbs.AbsGrhTrsPortQuery):
    IST_grh__trs_obj__queryraw_creator = GRH_TRS_OBJ_QUERYRAW_CREATOR

    def __init__(self, *args):
        self._initAbsGrhTrsPortQuery(*args)


class TrsNodeQuery(grhObjAbs.AbsGrhTrsNodeQuery):
    CLS_grh__trs_node_query__port_query_stack = _grhObjStack.TrsPortQueryStack
    CLS_grh__trs_node_query__port_query = TrsPortQuery

    IST_grh__trs_obj__queryraw_creator = GRH_TRS_OBJ_QUERYRAW_CREATOR

    def __init__(self, *args):
        self._initAbsGrhTrsNodeQuery(*args)


class TrsObjQueryBuilder(grhObjAbs.AbsGrhTrsObjQueryBuilder):
    CLS_grh__trs_node_query_builder__node_query_stack = _grhObjStack.TrsNodeQueryStack
    CLS_grh__trs_node_query_builder__node_query = TrsNodeQuery

    IST_grh__trs_node_query_builder__obj_queryraw_creator = GRH_TRS_OBJ_QUERYRAW_CREATOR

    def __init__(self, *args):
        self._initAbsGrhTrsObjQueryBuilder(*args)


GRH_TRS_OBJ_QUERY_BUILDER = TrsObjQueryBuilder(
    ar_mtx_configure.Util.GRAPHIC_NAME, mtxCfg.MtxUtility.DEF_mtx___graphic_name
)


class TrsObjQueue(grhObjAbs.AbsGrhObjQueue):
    CLS_grh__obj_queue__node_stack = _grhObjStack.TrsNodeStack

    def __init__(self, *args):
        self._initAbsGrhObjQueue(*args)


GRH_TRS_OBJ_QUEUE = TrsObjQueue()
