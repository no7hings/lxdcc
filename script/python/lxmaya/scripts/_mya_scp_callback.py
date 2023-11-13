# coding:utf-8
from lxbasic import bsc_core

import lxcontent.objects as ctt_objects

from lxmaya import ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class ScpCbkEnvironment(object):
    KEY = 'workspace environment build'

    def __init__(self):
        self._cfg = ctt_objects.Configure(
            value=bsc_core.RscConfigure.get_yaml(
                'katana/script/scene'
            )
        )
        self._cfg.set_flatten()

    @classmethod
    def save(cls, data):
        pass

    @classmethod
    def register(cls, data):
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            bsc_core.EnvironMtd.set(
                i_env_key, i_env_value
            )
            bsc_core.Log.trace_method_result(
                cls.KEY,
                'register: key="{}", value="{}"'.format(i_env_key, i_env_value)
            )

    def add_from_resolver(self, *args, **kwargs):
        if 'filename' in kwargs:
            f = kwargs['filename']
        else:
            f = mya_dcc_objects.Scene.get_current_file_path()
        #
        import lxresolver.scripts as rsv_scripts

        return rsv_scripts.ScpEnvironment.get_data(f)

    def add_from_work_environment(self, *args, **kwargs):
        import lxshotgun.scripts as stg_scripts

        task_id = bsc_core.EnvironMtd.get(
            'PAPER_TASK_ID'
        )
        return stg_scripts.ScpEnvironment.get_data(task_id)

    def add_from_scene(self, *args, **kwargs):
        return False, None

    @ma_core.Modifier.undo_run
    def execute(self, *args, **kwargs):
        if ma_core.get_is_ui_mode():
            fncs = [
                self.add_from_resolver,
                self.add_from_work_environment,
                self.add_from_scene,
            ]
        else:
            fncs = [
                self.add_from_resolver,
                self.add_from_work_environment,
                self.add_from_scene,
            ]

        for i_fnc in fncs:
            i_result, i_data = i_fnc(*args, **kwargs)
            if i_result is True:
                self.register(i_data)
                self.save(i_data)
                return True

        bsc_core.Log.trace_method_error(
            self.KEY, 'failed to load form any where'
        )
