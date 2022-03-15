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

    @classmethod
    def _get_rsv_asset_auto_(cls):
        import lxresolver.commands as rsv_commands
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_entity()
                return rsv_asset

    def set_run(self):
        self._ktn_workspace.set_workspace_create()
        #
        rsv_asset = self._get_rsv_asset_auto_()
        if rsv_asset is not None:
            role = rsv_asset.get('role')
            if role in ['chr']:
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
            else:
                ktn_core.VariablesSetting().set_register_by_configure(
                    {
                        'layer': ['master'],
                        'quality': ['low', 'med', 'hi', 'custom'],
                        'camera': ['full', 'half', 'add_0', 'add_1', 'asset_free', 'shot', 'shot_free'],
                        'light_pass': ['all'],
                        'look_pass': ['default', 'plastic', 'ambocc', 'wire'],
                        'variables_enable': ['on', 'off']
                    }
                )


