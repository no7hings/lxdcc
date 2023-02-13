# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
        # self.loader._label = "Test"
    # file-path has space
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        os_files = obj.get_file_plf_objs()
        for os_file in os_files:
            if ' ' in os_file.path:
                error_obj_files.append(os_file)
        #
        is_error = self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass
    # file-path exists
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        os_files = obj.get_file_plf_objs()
        for os_file in os_files:
            if os_file.get_is_exists() is False:
                error_obj_files.append(os_file)
        #
        is_error = self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        file_references = _mya_dcc_obj_objs.FileReferences().get_objs()
        self._set_objs_check_(file_references)
