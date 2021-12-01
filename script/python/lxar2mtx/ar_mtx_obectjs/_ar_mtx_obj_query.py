# coding:utf-8
from LxGraphic import grhCfg, grhObjAbs

from LxGraphic.grhObjects import _grhObjStack, _grhObjQuery

from .. import ar_mtx_configure, ar_mtx_abstract


class ObjLoader(ar_mtx_abstract.AbsDccObjLoader):
    def __init__(self, *args):
        self._initAbsDccObjLoader(*args)


class ObjQueryrawCreator(ar_mtx_abstract.AbsDccObjQueryrawCreator):
    CLS_grh__obj_query_creator__node_queryraw_stack = _grhObjStack.NodeQueryrawStack
    CLS_grh__obj_query_creator__node_queryraw = _grhObjQuery.NodeQueryraw

    CLS_grh__obj_query_creator__obj_loader = ObjLoader

    def __init__(self, *args):
        self._initAbsDccObjQueryrawCreator(*args)


GRH_OBJ_QUERYRAW_CREATOR = ObjQueryrawCreator()


class PortQuery(grhObjAbs.AbsGrhPortQuery):
    VAR_grh__port_query__portsep = grhCfg.GrhUtility.DEF_grh__node_port_pathsep

    IST_grh__obj_query__queryraw_creator = GRH_OBJ_QUERYRAW_CREATOR

    def __init__(self, *args):
        self._initAbsGrhPortQuery(*args)


class NodeQuery(grhObjAbs.AbsGrhNodeQuery):
    CLS_grh__node_query__port_query_stack = _grhObjStack.PortQueryStack
    CLS_grh__node_query__port_query = PortQuery

    IST_grh__obj_query__queryraw_creator = GRH_OBJ_QUERYRAW_CREATOR

    def __init__(self, *args):
        self._initAbsGrhNodeQuery(*args)


class ObjQueryBuilder(grhObjAbs.AbsGrhObjQueryBuilder):
    CLS_grh__obj_query_builder__node_query = NodeQuery
    CLS_grh__obj_query_builder__node_query_stack = _grhObjStack.NodeQueryStack

    def __init__(self, *args):
        self._initAbsGrhObjQueryBuilder(*args)


GRH_OBJ_QUERY_BUILDER = ObjQueryBuilder(
    ar_mtx_configure.Util.GRAPHIC_NAME
)


# object cache ******************************************************************************************************* #
class ObjQueue(ar_mtx_abstract.AbsDccObjQueue):
    CLS_grh__obj_queue__node_stack = _grhObjStack.NodeStack

    def __init__(self, *args):
        self._initAbsDccObjQueue(*args)


GRH_OBJ_QUEUE = ObjQueue()
