# coding:utf-8
import lxresolver.commands as rsv_commands


class AbsRsvObjHookOpt(object):
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

    def get_asset_render_output_directory(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-render-output-dir'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-render-output-dir'
        else:
            raise TypeError()

        render_output_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        rsv_render_output_directory_path = render_output_directory_rsv_unit.get_result(
            version=version
        )
        return rsv_render_output_directory_path
