# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    EXCEPT_DCC_PATHS = ['norender', 'LRC']
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # exists
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        is_error = obj.get_is_exists() and obj.path not in self.EXCEPT_DCC_PATHS
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_0(self, *args):
        obj = args[0]
        if obj.get_is_exists():
            obj.set_delete()

    def set_check_run(self):
        self.set_restore()
        nodes = _mya_dcc_obj_objs.DisplayLayers.get_custom_nodes(reference=False)
        self._set_objs_check_(nodes)
