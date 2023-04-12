# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxkatana import ktn_core


class ScpCbkEnvironment(object):
    KEY = 'workspace environment build'
    def __init__(self):
        self._cfg = bsc_objects.Configure(
            value=bsc_core.CfgFileMtd.get_yaml(
                'katana/script/scene'
            )
        )
        self._cfg.set_flatten()
    @classmethod
    def save(cls, data):
        workspace_setting = ktn_core.WorkspaceSetting()
        workspace_setting.build_env_ports()
        workspace_setting.build_look_ports()
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            workspace_setting.save_env(
                i_index, i_key, i_env_key, i_env_value
            )
    @classmethod
    def register(cls, data):
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            bsc_core.EnvironMtd.set(
                i_env_key, i_env_value
            )
            bsc_core.LogMtd.trace_method_result(
                cls.KEY,
                'register: key="{}", value="{}"'.format(i_env_key, i_env_value)
            )
    @classmethod
    def add_for_render(cls):
        pass

    def add_from_resolver(self, *args, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        data = []
        if 'filename' in kwargs:
            f = kwargs['filename']
        else:
            f = ktn_core.NodegraphAPI.GetProjectFile()
        #
        if f:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(f)
            if rsv_scene_properties:
                dict_ = rsv_scene_properties.get_value()
                keys = resolver.VariantTypes.All
                for i_key in keys:
                    if i_key in dict_:
                        i_env_key = 'PG_{}'.format(i_key.upper())
                        i_env_value = dict_[i_key]
                        data.append(
                            (i_key, i_env_key, i_env_value)
                        )
                #
                bsc_core.LogMtd.trace_method_result(
                    self.KEY,
                    'load from resolver'
                )
                return True, data
        return False, None

    def add_from_work_environment(self, *args, **kwargs):
        return False, None

    def add_from_scene(self, *args, **kwargs):
        workspace_setting = ktn_core.WorkspaceSetting()
        data = workspace_setting.get_env_data()
        if data:
            bsc_core.LogMtd.trace_method_result(
                self.KEY,
                'load from scene'
            )
            return True, data
        return False, None
    @ktn_core.Modifier.undo_run
    def execute(self, *args, **kwargs):
        if ktn_core.get_is_ui_mode():
            fncs = [
                self.add_from_work_environment,
                #
                self.add_from_resolver,
                self.add_from_scene,
            ]
        else:
            fncs = [
                self.add_from_resolver,
                self.add_from_scene,
            ]

        for i_fnc in fncs:
            i_result, i_data = i_fnc(*args, **kwargs)
            if i_result is True:
                self.register(i_data)
                self.save(i_data)
                return True

        bsc_core.LogMtd.trace_method_error(
            self.KEY, 'failed to load form any where'
        )


class ScpCbkGui(object):
    def __init__(self):
        pass
    @classmethod
    def refresh_tool_kit(cls):
        from lxutil_gui.qt import utl_gui_qt_core
        w = utl_gui_qt_core.get_session_window_by_name('dcc-tool-panels/gen-tool-kit')
        if w is not None:
            w.refresh_all()
    @classmethod
    def refresh_all(cls):
        cls.refresh_tool_kit()

    def execute(self, *args, **kwargs):
        self.refresh_all()
