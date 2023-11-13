# coding:utf-8
from lxusd.warp import *

from lxbasic import bsc_core

from lxusd import usd_configure

from lxutil import utl_core


class AbsUsdScene(object):
    def __init__(self, file_path, root=None):
        self._file_path = file_path
        self._root = root
        self._set_stage_create_()

    @classmethod
    def _set_stage_create_(cls):
        return Usd.Stage.CreateInMemory()

    @classmethod
    def _set_reference_add_(cls, stage, file_path, root):
        usd_root = stage.GetPseudoRoot()
        if root is not None:
            dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(root, pathsep=usd_configure.Obj.PATHSEP)
            if dag_path_comps:
                dag_path_comps.reverse()
            for i in dag_path_comps:
                if i != usd_configure.Obj.PATHSEP:
                    usd_root = stage.DefinePrim(i, '')
        #
        bsc_core.Log.trace_method_result(
            'usd-reference-add',
            u'file="{}"'.format(file_path)
        )
        usd_root.GetReferences().AddReference(file_path, usd_root.GetPath())
        stage.Flatten()
