# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Texture-file-name is Overlapping
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        os_files = obj.get_file_plf_objs()
        for os_file in os_files:
            os_normcase_file_path = os_file.normcase_path
            os_normcase_file_name = os_file.name
            if os_normcase_file_name in self._os_file_name_dict:
                os_normcase_file_paths = self._os_file_name_dict[os_normcase_file_name]
            else:
                os_normcase_file_paths = []
                self._os_file_name_dict[os_normcase_file_name] = os_normcase_file_paths

            if os_normcase_file_path not in os_normcase_file_paths:
                os_normcase_file_paths.append(os_normcase_file_path)

            if len(os_normcase_file_paths) > 1:
                error_obj_files.append(os_file)
        #
        is_error = self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs
    # Rename Texture-file-name & Repath Node
    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        self._os_normcase_file_paths = []
        self._os_file_name_dict = {}

        file_references = _mya_dcc_obj_objs.TextureReferences().get_objs()
        self._set_objs_check_(file_references)
