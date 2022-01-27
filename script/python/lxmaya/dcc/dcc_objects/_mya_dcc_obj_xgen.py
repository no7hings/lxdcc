# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .. import mya_dcc_obj_abs

from ...dcc.dcc_objects import _mya_dcc_obj_dag, _mya_dcc_obj_utility

import lxutil.dcc.dcc_objects as utl_dcc_objects


class XgnPalette(mya_dcc_obj_abs.AbsMyaFileReferenceObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    OS_FILE_CLASS = utl_dcc_objects.OsFile
    def __init__(self, path, file_path=None):
        super(XgnPalette, self).__init__(
            self._get_full_path_(path),
            file_path
        )


class XgnDescription(
    mya_dcc_obj_abs.AbsMyaFileReferenceObj,
    mya_dcc_obj_abs.AbsMaShapeDef,
):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    OS_FILE_CLASS = utl_dcc_objects.OsFile
    TRANSFORM_CLASS = _mya_dcc_obj_dag.Transform
    def __init__(self, path, file_path=None):
        super(XgnDescription, self).__init__(
            self._get_full_path_(path),
            file_path
        )
        self._set_ma_shape_def_init_(self.path)

    def get_is_multiply_reference(self):
        return True
