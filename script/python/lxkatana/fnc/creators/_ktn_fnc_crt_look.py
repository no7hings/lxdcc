# coding:utf-8
import copy

from lxkatana import ktn_core

from lxkatana.fnc.builders import _ktn_fnc_bdr_utility


class LookWorkspaceCreator(object):
    OPTION = dict(
        look_path='default'
    )
    def __init__(self, file_path=None, root=None, option=None):
        self._file_path = file_path
        self._root = root
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
        #
        self._ktn_workspace = _ktn_fnc_bdr_utility.AssetWorkspaceBuilder()

    def set_run(self):
        self._ktn_workspace.set_workspace_create()
        #
        ktn_core.VariablesSetting().set_register_by_configure(
            {
                'layer': ['master'],
                'quality': ['low', 'mid', 'hi'],
                'camera': ['full_body', 'upper_body', 'upper_body_35', 'upper_body_50', 'close_up', 'free'],
                'light_pass': ['all'],
                'look_pass': ['default'],
                'variables_enable': ['off', 'on'],
            }
        )


