# coding:utf-8
import lxresolver.commands as rsv_commands


class AbsRsvOHookOpt(object):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        self._rsv_scene_properties = rsv_scene_properties
        self._resolver = rsv_commands.get_resolver()
        self._rsv_task = self._resolver.get_rsv_task(
            **self._rsv_scene_properties.value
        )
        self._hook_option_opt = hook_option_opt
    @classmethod
    def get_resolver(cls):
        return rsv_commands.get_resolver()
