# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_dags


class Method(ma_fnc_abstract.AbsMyaChecker):
    NAMING_PATTERN = '{self.transform.name}*Shape'
    def __init__(self, *args):
        super(Method, self).__init__(*args)
        #
        # self.loader.descriptions = [
        #     {
        #         "Test": {
        #             "repair": {
        #                 "description": "Test A"
        #             }
        #         }
        #     }
        # ]

    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = not obj.get_is_naming_match(self.NAMING_PATTERN)
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        objs = _mya_dcc_obj_dags.Shapes().get_custom_nodes(reference=False)
        self._set_objs_check_(objs)
