# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxresolver.commands as rsv_commands


class ScpEnvironmentOpt(object):
    @classmethod
    def register_from_scene(cls, file_path):
        resolver = rsv_commands.get_resolver()
        keys = resolver.VariantTypes.All
        #
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
            file_path
        )
        if rsv_scene_properties:
            dict_ = rsv_scene_properties.get_value()
        else:
            dict_ = {}
        #
        for i_key in keys:
            i_env_key = 'PG_{}'.format(i_key.upper())
            #
            if i_key in dict_:
                i_env_value = dict_[i_key]
            else:
                i_env_value = ''
            #
            bsc_core.EnvironMtd.set(
                i_env_key, i_env_value
            )
    @classmethod
    def get_as_dict(cls):
        dict_ = {}
        resolver = rsv_commands.get_resolver()
        keys = resolver.VariantTypes.All
        for i_key in keys:
            i_env_key = 'PG_{}'.format(i_key.upper())
            dict_[i_key] = bsc_core.EnvironMtd.get(i_env_key) or ''
        return dict_


if __name__ == '__main__':
    pass
