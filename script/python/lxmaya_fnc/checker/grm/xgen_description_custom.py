# coding:utf-8
from lxmaya import ma_core

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs

import lxutil.dcc.dcc_objects as utl_dcc_objects


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # file exists
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        obj_path = obj.path
        #
        error_obj_files = []
        if obj_path in self._file_reference_dict:
            for port_path, file_path in self._file_reference_dict[obj_path]:
                os_file = utl_dcc_objects.OsFile(file_path)
                if os_file.get_is_exists() is False:
                    error_obj_files.append(os_file)
        #
        is_error = self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        self._file_reference_dict = ma_core._ma_type__get_file_reference_dict_('xgmDescription')
        nodes = _mya_dcc_obj_objs.XgenDescriptions.get_objs()
        self._set_objs_check_(nodes)
