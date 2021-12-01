# coding:utf-8
# graphic
from LxGraphic import grhCfg
# materialx
from LxMtx import mtxCfg, mtxObjects
# usd
from LxUsd import usdObjects
# usd2materialx
from .. import usd2mtxObjAbs

from ..usd2mtxObjects import _usd2mtxObjQuery


class ObjTranslator(usd2mtxObjAbs.AbsDcc2mtxObjTranslator):
    VAR_grh__obj_translator__channel_convert_dict = {
        mtxCfg.MtxUtility.DEF_mtx__datatype__color3: {
            grhCfg.GrhNodeQuery.typepath: u'float_to_rgb'
        },
        mtxCfg.MtxUtility.DEF_mtx__datatype__vector3: {
            grhCfg.GrhNodeQuery.typepath: u'float_to_rgb'
        },
        mtxCfg.MtxUtility.DEF_mtx__datatype__color4: {
            grhCfg.GrhNodeQuery.typepath: u'float_to_rgba'
        },
        mtxCfg.MtxUtility.DEF_mtx__datatype__vector4: {
            grhCfg.GrhNodeQuery.typepath: u'float_to_rgba'
        },
    }

    VAR_grh__obj_translator__src_node_pathsep = mtxCfg.MtxUtility.DEF_mya_node_pathsep
    VAR_grh__obj_translator__tgt_node_pathsep = mtxCfg.MtxUtility.DEF_mtx__node_pathsep

    IST_grh__obj_translator__obj_queryraw_creator = _usd2mtxObjQuery.GRH_TRS_OBJ_QUERYRAW_CREATOR
    IST_grh__obj_translator__obj_query_builder = _usd2mtxObjQuery.GRH_TRS_OBJ_QUERY_BUILDER

    def __init__(self, *args):
        self._initAbsDcc2mtxObjTranslator(*args)


class Node(usd2mtxObjAbs.AbsDcc2mtxNode):
    CLS_grh__trs_node__src_node = usdObjects.Node
    CLS_grh__trs_node__tgt_node = mtxObjects.Node

    CLS_grh__trs_node__obj_translator = ObjTranslator

    IST_grh__trs_node__obj_queryraw_creator = _usd2mtxObjQuery.GRH_TRS_OBJ_QUERYRAW_CREATOR
    IST_grh__trs_node__obj_query_builder = _usd2mtxObjQuery.GRH_TRS_OBJ_QUERY_BUILDER
    IST_grh__trs_node__obj_queue = _usd2mtxObjQuery.GRH_TRS_OBJ_QUEUE

    def __init__(self, *args):
        self._initAbsDcc2mtxNode(*args)


# proxy ************************************************************************************************************** #
class ShaderProxy(usd2mtxObjAbs.AbsDcc2mtxShaderProxy):
    CLS_grh__trs_node_proxy__trs_node = Node

    CLS_grh__trs_node_proxy__tgt_node_proxy = mtxObjects.ShaderProxy

    def __init__(self, *args, **kwargs):
        self._initAbsDcc2mtxShaderProxy(*args, **kwargs)


class MaterialProxy(usd2mtxObjAbs.AbsDcc2mtxMaterialProxy):
    CLS_grh__trs_node_proxy__trs_node = Node

    CLS_grh__trs_node_proxy__tgt_node_proxy = mtxObjects.MaterialProxy

    CLS_grh__trs_input_node_proxy = ShaderProxy

    VAR_grh__trs_material_proxy_surface_shader_portpath = [u'outputs:arnold:surface', u'outputs:surface']
    VAR_grh__trs_material_proxy_displacement_shader_portpath = [u'outputs:arnold:displacement', u'outputs:displacement']
    VAR_grh__trs_material_proxy_volume_shader_portpath = [u'outputs:arnold:volume', u'outputs:volume']

    def __init__(self, *args, **kwargs):
        self._initAbsDcc2mtxMaterialProxy(*args, **kwargs)


class GeometryProxy(usd2mtxObjAbs.AbsDcc2mtxGeometryProxy):
    CLS_grh__trs_node_proxy__trs_node = Node

    CLS_grh__trs_node_proxy__tgt_node_proxy = mtxObjects.GeometryProxy

    CLS_grh__trs_input_node_proxy = MaterialProxy

    VAR_grh__trs_src_material_portpath = u'material:binding'

    def __init__(self, *args, **kwargs):
        self._initAbsDcc2mtxGeometryProxy(*args, **kwargs)
