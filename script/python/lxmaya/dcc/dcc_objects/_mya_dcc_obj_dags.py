# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from ... import ma_core
from .. import mya_dcc_obj_abs

from ...dcc.dcc_objects import _mya_dcc_obj_dag, _mya_dcc_obj_geometry


class Groups(mya_dcc_obj_abs.AbsMyaObjs):
    DCC_NODE_CLASS = _mya_dcc_obj_dag.Group
    def __init__(self, *args):
        super(Groups, self).__init__(*args)
    @classmethod
    def get_paths(cls, reference=True, exclude_paths=None):
        def set_exclude_filter_fnc_(paths):
            if exclude_paths is not None:
                [paths.remove(_i) for _i in exclude_paths if _i in paths]
            return paths

        _ = ma_core._ma__get_group_paths_()
        if exclude_paths is not None:
            return set_exclude_filter_fnc_(_)
        if reference is True:
            return _
        return set_exclude_filter_fnc_(
            [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
        )


class Shapes(mya_dcc_obj_abs.AbsMyaObjs):
    DCC_NODE_CLASS = _mya_dcc_obj_dag.Shape
    def __init__(self, *args):
        super(Shapes, self).__init__(*args)
    @classmethod
    def get_paths(cls, reference=True, exclude_paths=None):
        def set_exclude_filter_fnc_(paths):
            if exclude_paths is not None:
                [paths.remove(_i) for _i in exclude_paths if _i in paths]
            return paths

        _ = ma_core._ma__get_shape_paths_()
        if exclude_paths is not None:
            return set_exclude_filter_fnc_(_)
        if reference is True:
            return _
        return set_exclude_filter_fnc_(
            [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
        )


class Geometries(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = [
        'mesh',
        'nurbsCurve',
        'nurbsSurface'
    ]
    #
    DCC_NODE_CLASS = _mya_dcc_obj_dag.Shape
    def __init__(self, *args):
        super(Geometries, self).__init__(*args)


class Meshes(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = [
        'mesh',
    ]
    #
    DCC_NODE_CLASS = _mya_dcc_obj_geometry.Mesh
    def __init__(self, *args):
        super(Meshes, self).__init__(*args)
