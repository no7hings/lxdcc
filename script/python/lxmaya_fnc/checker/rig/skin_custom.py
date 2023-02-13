# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_obj


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # animation
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        is_error = not obj.get_port('envelope')
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        nodes = [_mya_dcc_obj_obj.Node(i) for i in cmds.ls(type='skinCluster', long=1)]
        self._set_objs_check_(nodes)
