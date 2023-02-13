# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    #
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        os_files = obj.get_file_plf_objs()
        for os_file in os_files:
            if not os_file.ext == '.tx':
                error_obj_files.append(os_file)
        #
        self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        color_space = obj.get_port('colorSpace').get()
        os_files = obj.get_file_plf_objs()
        for os_file in os_files:
            key = os_file.name
            if key not in self._color_space_dict:
                color_spaces = []
                self._color_space_dict[key] = color_spaces
            else:
                color_spaces = self._color_space_dict[key]
            #
            if color_space not in color_spaces:
                color_spaces.append(color_space)
            #
            if len(color_spaces) > 1:
                error_obj_files.append(os_file)
        #
        self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        #
        self._color_space_dict = {}
        #
        file_references = _mya_dcc_obj_objs.TextureReferences().get_objs()
        self._set_objs_check_(file_references)
