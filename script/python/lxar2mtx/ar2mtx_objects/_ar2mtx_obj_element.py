# coding:utf-8
from LxMtx import mtxObjects

from .. import ar2mtx_abstract

from ..ar2mtx_objects import _ar2mtx_obj_node


class Look(ar2mtx_abstract.AbsDcc2mtxLook):
    CLS_mtx__trs_look__tgt_look = mtxObjects.Look
    CLS_mtx__trs_look__trs_geometry_proxy = _ar2mtx_obj_node.GeometryProxy
    def __init__(self, *args):
        self._initAbsDcc2mtxLook(*args)
