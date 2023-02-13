# coding:utf-8
from lxmaya import ma_core

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_obj, _mya_dcc_obj_objs


# /utl/node_custom
class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Node-type is Unknown
    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = obj.get_is_exists()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # Delete Node
    def _repair_method_0(self, *args):
        obj = args[0]
        if obj.get_is_exists():
            obj.set_delete()
    # Node-name is Overlapping
    def _check_method_1(self, *args):
        obj, check_index = args
        #
        is_error = obj.get_is_exists()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # Rename Node-name
    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        unknown_nodes = _mya_dcc_obj_objs.UnknownNodes().get_custom_nodes(reference=False)
        self._set_objs_check_(unknown_nodes, [0])
        #
        naming_overlapped_nodes = [_mya_dcc_obj_obj.Node(i) for i in ma_core._ma_get_override_node_paths_(reference=False)]
        self._set_objs_check_(naming_overlapped_nodes, [1])
