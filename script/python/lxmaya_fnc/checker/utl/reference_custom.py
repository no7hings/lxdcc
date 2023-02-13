# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # naming
    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = obj.get_is_loaded() is False
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        references = _mya_dcc_obj_objs.References.get_custom_nodes(reference=False)
        self._set_objs_check_(references)
