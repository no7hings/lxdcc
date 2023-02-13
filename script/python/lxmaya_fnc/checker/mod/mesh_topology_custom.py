# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_dag, _mya_dcc_obj_geometry


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # face zero area
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_face_zero_area_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass
    # edge zero length
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_edge_zero_length_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass
    # face n-side
    def _check_method_2(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_face_n_side_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_2(self, *args):
        pass
    # face non-triangulable
    def _check_method_3(self, *args):
        obj, check_index = args[:2]

        #
        error_obj_comps = []
        comp_names = obj.get_face_non_triangulable_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_3(self, *args):
        pass
    # face holed
    def _check_method_4(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_face_holed_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_4(self, *args):
        pass
    # face lamina
    def _check_method_5(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_face_lamina_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_5(self, *args):
        pass
    # edge open
    def _check_method_6(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_edge_open_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_6(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        root = _mya_dcc_obj_dag.Group('|master|hi')
        mesh_paths = root.get_all_shape_paths(include_obj_type='mesh')
        mesh_objs = [_mya_dcc_obj_geometry.Mesh(i) for i in mesh_paths]
        self._set_objs_check_(mesh_objs)
