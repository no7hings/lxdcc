# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_dags


class Method(ma_fnc_abstract.AbsMyaChecker):
    NAMING_PATTERN = '*_grp'
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Group-name is Non-match *_grp
    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = not obj.get_is_naming_match(self.NAMING_PATTERN)
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_0(self, *args):
        obj = args[0]
        obj._set_path_update_()
        if obj.get_is_exists():
            new_name = '{}_grp'.format(obj.name)
            obj.set_rename(new_name)
    # empty
    def _check_method_1(self, *args):
        obj, check_index = args
        #
        is_error = not obj.get_all_shape_paths()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_1(self, *args):
        obj = args[0]
        obj._set_path_update_()
        if obj.get_is_exists():
            obj.set_delete()

    def set_check_run(self):
        pass
