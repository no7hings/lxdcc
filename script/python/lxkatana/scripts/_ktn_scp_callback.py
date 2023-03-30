# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxkatana import ktn_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxresolver.commands as rsv_commands


class ScpCbkEnvironment(object):
    RSV_MAPPER = dict(
        root='PG_ROOT',
        project='PG_PROJECT',
        workspace='PG_WORKSPACE',
        branch='PG_BRANCH',
        role='PG_ROLE',
        sequence='PG_SEQUENCE',
        asset='PG_ASSET',
        shot='PG_SHOT',
        resource='PG_RESOURCE',
        #
        step='PG_STEP',
        #
        task='PG_TASK',
        task_extra='PG_TASK_EXTRA',
        #
        version='PG_VERSION',
        version_extra='PG_VERSION_EXTRA',
        #
        artist='PG_ARTIST',
    )
    def __init__(self):
        self._cfg = bsc_objects.Configure(
            value=bsc_core.CfgFileMtd.get_yaml(
                'katana/script/scene'
            )
        )
        self._cfg.set_flatten()

        self._rsv_scene_properties_mapper = self._cfg.get(
            'option.rsv_scene_properties_mapper'
        )

    def write_to_scene(self):
        pass

    def read_from_scene(self):
        pass

    def add_from_resolver(self, *args, **kwargs):
        f = kwargs['filename']
        if f:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(f)
            if rsv_scene_properties:
                workspace_setting = ktn_core.WorkspaceSetting()
                workspace_setting.build_environment_ports()
                #
                dict_ = rsv_scene_properties.get_value()
                i_index = 0
                for i_k, i_env_key in self._rsv_scene_properties_mapper.items():
                    if i_k in dict_:
                        i_env_value = dict_[i_k]
                        bsc_core.EnvironMtd.set(
                            i_env_key, i_env_value
                        )
                        workspace_setting.register_environment(
                            i_index, i_env_key, i_env_value
                        )
                        i_index += 1
                return True
        return False

    def add_from_work_environment(self, *args, **kwargs):
        return False

    def add_from_scene(self, *args, **kwargs):
        return False

    def execute(self, *args, **kwargs):
        fncs = [
            self.add_from_work_environment,
            self.add_from_resolver,
            self.add_from_scene
        ]
        for i_fnc in fncs:
            i_result = i_fnc(*args, **kwargs)
            if i_result is True:
                return True

        bsc_core.LogMtd.trace_method_error(
            'environment build', 'failed to build environment form any where'
        )
