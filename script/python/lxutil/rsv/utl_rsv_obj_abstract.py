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

    def get_asset_katana_render_file(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-scene-file'
            keyword_1 = 'asset-katana-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-scene-file'
            keyword_1 = 'asset-output-katana-scene-src-file'
        else:
            raise TypeError()

        render_use_scene = self._hook_option_opt.get_as_boolean('render_use_scene')
        if render_use_scene is True:
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            return scene_file_path
        else:
            render_us_scene_src = self._hook_option_opt.get_as_boolean('render_us_scene_src')
            if render_us_scene_src is True:
                scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword_1
                )
                scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
                return scene_src_file_path

    def get_asset_katana_render_output_directory(self):
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

    def get_asset_katana_video_all_mov_file(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-render-video-all-mov-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-render-video-all-mov-file'
        else:
            raise TypeError()

        render_output_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        rsv_render_output_directory_path = render_output_directory_rsv_unit.get_result(
            version=version, extend_variants=dict(variant='main')
        )
        return rsv_render_output_directory_path

    def get_exists_asset_review_mov_file(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword = 'asset-review-mov-file'
        elif workspace == 'output':
            keyword = 'asset-output-review-mov-file'
        else:
            raise TypeError()
        #
        review_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        return review_mov_file_rsv_unit.get_exists_result(
            version=version
        )
    @classmethod
    def get_dcc_args(cls, any_scene_file_path, application):
        resolver = rsv_commands.get_resolver()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
            any_scene_file_path
        )
        if rsv_scene_properties:
            if rsv_scene_properties.get('application') == application:
                return rsv_scene_properties
            #
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            #
            if workspace == 'publish':
                keyword = 'asset-{application}-scene-src-file'
            elif workspace == 'output':
                keyword = 'asset-output-{application}-scene-src-file'
            else:
                raise TypeError()

            keyword = keyword.format(**dict(application=application))

            rsv_task = resolver.get_rsv_task(
                **rsv_scene_properties.value
            )

            scene_src_file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            scene_src_file_path = scene_src_file_rsv_unit.get_exists_result(
                version=version
            )
            if scene_src_file_path is not None:
                return resolver.get_rsv_scene_properties_by_any_scene_file_path(
                    scene_src_file_path
                )

    def get_look_pass_names(self):
        import os
        #
        import fnmatch

        from lxbasic import bsc_core
        #
        step = self._rsv_scene_properties.get('step')
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'work':
            return ['default']
        elif workspace == 'publish':
            keyword = 'asset-look-klf-file'
        elif workspace == 'output':
            keyword = 'asset-output-look-klf-file'
        else:
            raise TypeError()
        #
        file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        file_path = file_rsv_unit.get_exists_result(
            version=version
        )

        if file_path:
            element_names = bsc_core.ZipFileOpt(file_path).get_element_names()
            look_pass_names = [os.path.splitext(i)[0] for i in fnmatch.filter(element_names, '*.klf')]
            return look_pass_names
        return ['default']