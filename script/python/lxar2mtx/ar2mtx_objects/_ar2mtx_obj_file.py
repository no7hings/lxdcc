# coding:utf-8
from LxMtx import mtxObjects

from .. import ar2mtx_abstract

from ..ar2mtx_objects import _ar2mtx_obj_query, _ar2mtx_obj_element


class File(ar2mtx_abstract.AbsDcc2mtxFile):
    CLS_mtx__trs_file__tgt_file = mtxObjects.File
    CLS_mtx__trs_file__trs_look = _ar2mtx_obj_element.Look

    IST_mtx__trs_file__trs_obj_queue = _ar2mtx_obj_query.GRH_TRS_OBJ_QUEUE

    def __init__(self, *args):
        self._initAbsDcc2mtxFile(*args)
