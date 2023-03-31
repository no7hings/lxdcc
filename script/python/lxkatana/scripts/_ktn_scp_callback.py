# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxkatana import ktn_core


class ScpCbkEnvironment(object):
    KEY = 'workspace environment'
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
        f = kwargs['filename']
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


class ScpCbkRender(object):
    def __init__(self):
        pass

    def get_kwargs_from_scene(self):
        p = bsc_objects.Content()
        workspace_setting = ktn_core.WorkspaceSetting()
        data = workspace_setting.get_env_data()
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            print i_key, i_env_key, i_env_value
            p.set(i_key, i_env_value)
        return p

    def refresh_all_render_Layers_version(self):
        from lxkatana.scripts import _ktn_scp_macro_extra

        version_key = 'render_version'

        nodes = ktn_core.NGObjsMtd.find_nodes_by_port_filters(
            type_name='Group', filters=[('type', 'RenderLayer_Wsp')]
        )
        for i_node in nodes:
            i_obj_opt = ktn_core.NGObjOpt(i_node)
            i_scp = _ktn_scp_macro_extra.ScpWspRenderLayer(i_node)
            i_kwargs = i_scp.get_variants()
            i_directory_p = i_obj_opt.get('parameters.render.output_directory')
            i_directory_p_opt = bsc_core.PtnParseOpt(i_directory_p)
            i_version_string = i_kwargs.pop(version_key)
            if bsc_core.PtnVersion.get_is_valid(i_version_string):
                continue
            #
            i_directory_p_opt.set_update(**i_kwargs)
            #
            i_version_kwargs = {}
            if i_version_string == 'new':
                i_version = i_directory_p_opt.get_new_version(version_key='render_version')
            elif i_version_string == 'latest':
                i_version = i_directory_p_opt.get_latest_version(version_key='render_version')
            else:
                raise RuntimeError()
            #
            i_version_kwargs[version_key] = i_version
            i_obj_opt.set('parameters.render.version', i_version)

    def execute(self, *args, **kwargs):
        if ktn_core.get_is_ui_mode():
            self.refresh_all_render_Layers_version()
