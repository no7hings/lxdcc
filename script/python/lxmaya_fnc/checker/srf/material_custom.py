# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # naming override
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        is_error = False
        assign_dict = obj.get_assign_dict()
        if 'obj_cmp' in assign_dict:
            _ = assign_dict['obj_cmp']
            is_error = True
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        shading_engines = _mya_dcc_obj_objs.Materials().get_custom_nodes()
        self._set_objs_check_(shading_engines)
