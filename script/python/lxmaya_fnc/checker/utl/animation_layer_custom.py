# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Animation-layer is Not Allowed
    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = obj.get_is_exists()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # Delete Animation-layer
    def _repair_method_0(self, *args):
        obj = args[0]
        obj._set_path_update_()
        if obj.get_is_exists():
            obj.set_delete()

    def set_check_run(self):
        self.set_restore()
        nodes = _mya_dcc_obj_objs.AnimationLayers.get_custom_nodes(reference=False)
        self._set_objs_check_(nodes)
