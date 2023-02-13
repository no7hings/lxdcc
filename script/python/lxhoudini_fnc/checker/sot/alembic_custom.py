# coding:utf-8
from lxhoudini_fnc import hou_fnc_abstract

import lxhoudini.dcc.dcc_objects as hou_dcc_objects


class Method(hou_fnc_abstract.AbsHouIspOp):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    #
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        materialx_paths = obj.get_materialx_geometry_paths()
        alembic_paths = obj.get_geometry_paths()
        if materialx_paths and alembic_paths:
            for path in materialx_paths:
                if path not in alembic_paths:
                    error_obj_comps.append(path)

        self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs
    #
    def _repair_method_0(self, *args):
        pass

    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        materialx_paths = obj.get_materialx_geometry_paths()
        alembic_paths = obj.get_geometry_paths()
        if materialx_paths and alembic_paths:
            for path in alembic_paths:
                if path not in materialx_paths:
                    error_obj_comps.append(path)

        self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs
    #
    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()

        alembics = []
        _ = hou_dcc_objects.Alembics().get_objs()
        for i in _:
            # filter alembic is from shot
            if i.get_is_naming_match('shot_gmt_abc'):
                parent = i.get_parent()
                if parent is not None:
                    # filter alembic is from variant "hi"
                    if parent.get_is_naming_match('*__gmt_abc__hi'):
                        alembics.append(i)
        self._set_objs_check_(alembics)
