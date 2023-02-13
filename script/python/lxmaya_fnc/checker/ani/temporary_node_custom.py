# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_obj, _mya_dcc_obj_objs


class Method(ma_fnc_abstract.AbsMyaChecker):
    DISPLAY_LAYER_PATHS = ['norender', 'LRC']
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # exists
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        is_error = obj.get_is_exists() and obj.path not in self._white_paths
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()

        nodes = _mya_dcc_obj_objs.TemporaryNodes().get_custom_nodes(reference=False)
        display_layers = [_mya_dcc_obj_obj.DisplayLayer(i) for i in self.DISPLAY_LAYER_PATHS]
        self._white_paths = []
        for i in display_layers:
            for j in i.get_objs():
                child_paths = j.get_descendant_paths()
                for child_path in child_paths:
                    if child_path not in self._white_paths:
                        self._white_paths.append(child_path)
        #
        self._set_objs_check_(nodes)
