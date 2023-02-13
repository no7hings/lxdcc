# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_obj, _mya_dcc_obj_dag


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # animation
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_node_paths = obj.get_source_node_paths(include_types=['animCurve'])
        error_sources = []
        for node_path in error_node_paths:
            error_node = _mya_dcc_obj_obj.Node(node_path)
            error_sources.append(error_node)
        #
        is_error = self.set_error_obj_sources_update(obj, check_index, error_sources)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass
    # transformation
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        is_error = not obj.get_transformations() == obj.DEFAULT_TRANSFORMATION
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        sets = cmds.ls('*_controllers_grp', type='objectSet', long=1)
        node_paths = [j for i in sets for j in cmds.sets(i, query=1) or [] if cmds.nodeType(j) == 'transform']
        nodes = [_mya_dcc_obj_dag.Transform(i) for i in node_paths]
        self._set_objs_check_(nodes)
