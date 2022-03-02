# coding:utf-8
import copy

from lxkatana import ktn_core

from lxkatana.fnc.builders import _ktn_fnc_bdr_utility

from lxutil.fnc import utl_fnc_obj_abs


class LookWorkspaceCreator(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        localtion='',
        look_path='default'
    )
    def __init__(self, option=None):
        super(LookWorkspaceCreator, self).__init__(option)
        #
        print self.get('location')
        self._ktn_workspace = _ktn_fnc_bdr_utility.AssetWorkspaceBuilder(
            self.get('location')
        )

    def set_run(self):
        self._ktn_workspace.set_workspace_create()
        #
        ktn_core.VariablesSetting().set_register_by_configure(
            {
                'layer': ['master'],
                'quality': ['low', 'med', 'hi', 'custom'],
                'camera': ['full_body', 'upper_body', 'upper_body_35', 'upper_body_50', 'close_up', 'add_0', 'add_1', 'asset_free', 'shot', 'shot_free'],
                'light_pass': ['all'],
                'look_pass': ['default', 'plastic', 'ambocc', 'wire'],
                'variables_enable': ['on', 'off']
            }
        )


