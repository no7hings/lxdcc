# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_obj, _mya_dcc_obj_dags

from lxmaya.modifiers import _mya_mdf_utility


# dag/geometry
class Method(ma_fnc_abstract.AbsMyaChecker):
    NAMING_PATTERN = '*_geo'
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Geometry-transform-name is Non-match *_geo
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        is_error = not obj.transform.get_is_naming_match(self.NAMING_PATTERN)
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
            transform = obj.transform
            transform._set_path_update_()
            new_name = '{}_geo'.format(transform.name)
            transform.set_rename(new_name)
    # Geometry-transform-transformation(Translate, Rotate, Scale) is Non-default
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        is_error = obj.transform.get_matrix_is_changed()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass
    # shape instance
    def _check_method_2(self, *args):
        obj, check_index = args[:2]
        #
        is_error = obj.get_is_instanced()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_2(self, *args):
        pass
    # shape history
    def _check_method_3(self, *args):
        obj, check_index = args[:2]
        #
        error_node_paths = obj.get_history_paths()
        error_sources = []
        for node_path in error_node_paths:
            error_node = _mya_dcc_obj_obj.Node(node_path)
            error_sources.append(error_node)

        is_error = self.set_error_obj_sources_update(obj, check_index, error_sources)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    @_mya_mdf_utility.set_undo_mark_mdf
    def _repair_method_3(self, *args):
        obj = args[0]
        obj._set_path_update_()
        if obj.get_is_exists():
            obj.set_history_clear()

    def set_check_run(self):
        self.set_restore()
        geometries = _mya_dcc_obj_dags.Geometries().get_custom_nodes(reference=False)
        self._set_objs_check_(geometries)
