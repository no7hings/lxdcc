# coding:utf-8
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.cmds as cmds
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om2

from lxmaya.dcc.dcc_objects import _ma_dcc_obj_dag


class XgenDescription(_ma_dcc_obj_dag.Shape):
    def __init__(self, path):
        super(XgenDescription, self).__init__(path)
