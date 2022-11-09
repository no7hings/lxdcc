# coding:utf-8
from lxkatana import ktn_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

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
        self._ktn_workspace = ktn_dcc_objects.AssetWorkspace(
            self.get('location')
        )

    @classmethod
    def _get_rsv_asset_auto_(cls):
        import lxresolver.commands as rsv_commands
        #
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_resource()
                return rsv_asset

    def set_run(self):
        self._ktn_workspace.set_workspace_create()
        self._ktn_workspace.set_variables_registry()
        #
        # rsv_asset = self._get_rsv_asset_auto_()
        # if rsv_asset is not None:
        #     ktn_core.VariablesSetting().set_register_by_configure(
        #         {
        #             'layer': ['master', 'no_hair'],
        #             'quality': ['low', 'med', 'hi', 'custom'],
        #             'camera': ['full_body', 'upper_body', 'close_up', 'add_0', 'add_1', 'asset_free', 'shot', 'shot_free'],
        #             'light_pass': ['all'],
        #             'look_pass': ['default', 'plastic', 'ambocc', 'wire', 'white'],
        #             'variables_enable': ['on', 'off']
        #         }
        #     )


