# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_utility, _mya_dcc_obj_dag


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Step-group(s) is Non-exists
    def _check_method_0(self, *args):
        step_obj, check_index = args[:2]
        #
        asset_group_path = step_obj.get_variant('self.asset.dcc_path')
        step_group_paths = step_obj.get_variant('self.step.dcc_group_paths') or []
        #
        error_obj_comps = []
        if step_group_paths:
            for sub_group_path in step_group_paths:
                group = _mya_dcc_obj_dag.Group(sub_group_path)
                if group.get_is_exists() is False:
                    error_obj_comps.append(group)
        #
        obj = _mya_dcc_obj_dag.Group(asset_group_path)
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass
    # Base-group is Not Allowed
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        asset_group_path = obj.get_variant('self.asset.dcc_path')
        base_group = _mya_dcc_obj_dag.Group('{}|base'.format(asset_group_path))
        #
        is_error = base_group.get_is_exists() is True
        #
        if is_error is True:
            self.set_error_obj_raw_add(base_group, check_index)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        pass
