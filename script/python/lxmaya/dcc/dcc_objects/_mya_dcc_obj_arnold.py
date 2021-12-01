# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxutil.commands as utl_cmds

from .. import mya_dcc_obj_abs

from ...dcc.dcc_objects import _ma_dcc_obj_os, _ma_dcc_obj_utility


class AndMaterialx(mya_dcc_obj_abs.AbsMyaFileReferenceObj):
    PORT_CLASS = _ma_dcc_obj_utility.Port
    OS_FILE_CLASS = _ma_dcc_obj_os.OsFile
    def __init__(self, path):
        super(AndMaterialx, self).__init__(path)

    def get_file_plf_objs(self):
        lis = []
        for port_dcc_path, file_plf_path in self._reference_raw.items():
            lis.append(
                self._set_file_create_(file_plf_path, port_dcc_path)
            )
            mtx_reader = utl_cmds.MaterialxReader(file_plf_path)
            for i in mtx_reader.texture_paths:
                lis.append(
                    self._set_file_create_(i)
                )
        return lis


class AndStringReplace(mya_dcc_obj_abs.AbsMyaObj):
    PORT_CLASS = _ma_dcc_obj_utility.Port
    def __init__(self, path):
        super(AndStringReplace, self).__init__(path)
