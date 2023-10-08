# coding:utf-8
import lxcontent.objects as ctt_objects

from lxresolver import rsv_configure

import lxresolver.commands as rsv_commands

import copy


# todo: old method need clear or replace
class AbsAssetQuery(object):
    CONFIGURE_FILE_PATH = rsv_configure.Data.ASSET_CONFIGURE_PATH
    def __init__(self, task_properties):
        self._task_properties = task_properties
        application = task_properties.get('application')
        #
        self._file_configure = ctt_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        self._file_configure.set('option.application', application)
        self._file_configure.set_flatten()
        self._resolver = rsv_commands.get_resolver()

    def _get_result_(self, key, sub_key, **kwargs):
        task_properties = self._task_properties
        resolver = self._resolver
        #
        definition_kwargs = self._file_configure.get('{}.{}'.format(key, sub_key))
        custom_kwargs = kwargs
        #
        _kwargs = copy.copy(
            task_properties.value
        )
        if definition_kwargs is None:
            return None
        #
        for k, v in definition_kwargs.items():
            _kwargs[k] = v
        #
        for k, v in custom_kwargs.items():
            if k in _kwargs:
                _kwargs[k] = v
            else:
                _kwargs[k] = v
        #
        rsv_task = resolver.get_rsv_task(**self._task_properties.value)
        rsv_unit = rsv_task.get_rsv_unit(
            **_kwargs
        )
        if rsv_unit:
            extend_var_keys = rsv_task.rsv_project.get_value('extent-var-keys')
            extend_variants = {}
            for k, v in custom_kwargs.items():
                if k in extend_var_keys:
                    extend_variants[k] = v
            #
            if _kwargs['version'] == 'all':
                result = rsv_unit.get_result(
                    version='all',
                    extend_variants=extend_variants,
                    trim=(-5, None)
                )
            else:
                result = rsv_unit.get_result(
                    version=_kwargs['version'],
                    extend_variants=extend_variants
                )
            return result

    def _get_results_(self, key, sub_key, **kwargs):
        task_properties = self._task_properties
        resolver = self._resolver
        #
        definition_kwargs = self._file_configure.get('{}.{}'.format(key, sub_key))
        custom_kwargs = kwargs
        #
        _kwargs = copy.copy(
            task_properties.value
        )
        #
        for k, v in definition_kwargs.items():
            _kwargs[k] = v
        #
        for k, v in custom_kwargs.items():
            if k in _kwargs:
                _kwargs[k] = v
            else:
                _kwargs[k] = v
        #
        rsv_task = resolver.get_rsv_task(**self._task_properties.value)
        rsv_unit = rsv_task.get_rsv_unit(
            **_kwargs
        )
        if rsv_unit:
            return rsv_unit.get_results(
                version=_kwargs['version']
            )

    def _get_file_args_(self, key, sub_key, **kwargs):
        task_properties = self._task_properties
        resolver = self._resolver
        #
        definition_kwargs = self._file_configure.get('{}.{}'.format(key, sub_key))
        custom_kwargs = kwargs
        #
        _kwargs = copy.copy(
            task_properties.value
        )
        #
        for k, v in definition_kwargs.items():
            _kwargs[k] = v
        #
        for k, v in custom_kwargs.items():
            if k in _kwargs:
                _kwargs[k] = v
            else:
                _kwargs[k] = v
        #
        rsv_task = resolver.get_rsv_task(**self._task_properties.value)
        rsv_unit = rsv_task.get_rsv_unit(
            **_kwargs
        )
        lis = []
        if rsv_unit:
            results = rsv_unit.get_results(
                version=_kwargs['version']
            )
            if results:
                for i_result in results:
                    extend_variants = rsv_unit.get_extend_variants(i_result)
                    lis.append(
                        (i_result, extend_variants)
                    )
        return lis

    def _project__get_rsv_unit_(self, key, sub_key, **kwargs):
        task_properties = self._task_properties
        resolver = self._resolver
        #
        definition_kwargs = self._file_configure.get('{}.{}'.format(key, sub_key))
        custom_kwargs = kwargs
        #
        _kwargs = copy.copy(
            task_properties.value
        )
        #
        for k, v in definition_kwargs.items():
            _kwargs[k] = v
        #
        for k, v in custom_kwargs.items():
            if k in _kwargs:
                _kwargs[k] = v
            else:
                _kwargs[k] = v
        #
        rsv_task = resolver.get_rsv_task(**self._task_properties.value)
        return rsv_task.get_rsv_unit(
            **_kwargs
        )


class RsvAssetSceneQuery(AbsAssetQuery):
    KEY = 'main'
    def __init__(self, task_properties):
        super(RsvAssetSceneQuery, self).__init__(task_properties)

    def get(self, sub_key, **kwargs):
        return self._get_result_(self.KEY, sub_key, **kwargs)

    def get_work_cache_directory(self, **kwargs):
        sub_key = 'directory.work-cache-directory'
        return self.get(sub_key, **kwargs)

    def get_cache_directory(self):
        platform = self._task_properties.get('platform')
        if platform == 'windows':
            return 'l:/temp/cache/asset-comparer'
        elif platform == 'linux':
            return '/l/temp/cache/asset-comparer'

    def get_task_version_directory(self, **kwargs):
        sub_key = 'directory.task-version-directory'
        return self.get(sub_key, **kwargs)

    def get_task_no_version_directory(self, **kwargs):
        sub_key = 'directory.task-no-version-directory'
        return self.get(sub_key, **kwargs)

    def get_file(self, **kwargs):
        application = self._task_properties.get('application')
        sub_key = 'scene.{}-file'.format(application)
        return self.get(sub_key, **kwargs)

    def get_maya_file(self, **kwargs):
        sub_key = 'scene.maya-file'
        return self.get(sub_key, **kwargs)

    def get_maya_src_file(self, **kwargs):
        sub_key = 'scene.maya-src-file'
        return self.get(sub_key, **kwargs)

    def get_work_maya_src_file(self, **kwargs):
        sub_key = 'scene.work-maya-src-file'
        return self.get(sub_key, **kwargs)

    def get_houdini_file(self, **kwargs):
        sub_key = 'scene.houdini-file'
        return self.get(sub_key, **kwargs)

    def get_houdini_src_file(self, **kwargs):
        sub_key = 'scene.houdini-src-file'
        return self.get(sub_key, **kwargs)

    def get_katana_file(self, **kwargs):
        sub_key = 'scene.katana-file'
        return self.get(sub_key, **kwargs)

    def get_katana_src_file(self, **kwargs):
        sub_key = 'scene.katana-src-file'
        return self.get(sub_key, **kwargs)

    def get_surface_cfx_katana_src_file(self, **kwargs):
        sub_key = 'scene.surface-cfx-katana-src-file'
        return self.get(sub_key, **kwargs)

    def get_surface_cfx_maya_src_file(self, **kwargs):
        sub_key = 'scene.surface-cfx-maya-src-file'
        return self.get(sub_key, **kwargs)

    def get_src_file(self, **kwargs):
        application = self._task_properties.get('application')
        sub_key = 'scene.{}-src-file'.format(application)
        return self.get(sub_key, **kwargs)

    def get_render_output_dir(self, **kwargs):
        sub_key = 'render.output-dir'
        return self.get(sub_key, **kwargs)

    def get_output_render_dir(self, **kwargs):
        sub_key = 'render.output-render-dir'
        return self.get(sub_key, **kwargs)

    def get_render_maya_scene_file(self, **kwargs):
        sub_key = 'render.maya-scene-file'
        return self.get(sub_key, **kwargs)

    def get_render_katana_scene_file(self, **kwargs):
        sub_key = 'render.katana-scene-file'
        return self.get(sub_key, **kwargs)

    def get_render_katana_output_dir(self, **kwargs):
        sub_key = 'render.katana-output-dir'
        return self.get(sub_key, **kwargs)

    def get_preview_mov_file(self, **kwargs):
        sub_key = 'preview.mov-file'
        return self.get(sub_key, **kwargs)

    def get_review_mov_file(self, **kwargs):
        sub_key = 'review.mov-file'
        return self.get(sub_key, **kwargs)

    def get_camera_yml_file(self, **kwargs):
        sub_key = 'camera.yml-file'
        return self.get(sub_key, **kwargs)

    def get_camera_presp_abc_file(self, **kwargs):
        sub_key = 'camera.abc-file'
        return self.get(sub_key, **kwargs)

    def get_deadline_job_file(self, **kwargs):
        sub_key = 'deadline.job-file'
        return self.get(sub_key, **kwargs)


class RsvAssetGeometryQuery(AbsAssetQuery):
    KEY = 'geometries'
    def __init__(self, task_properties):
        super(RsvAssetGeometryQuery, self).__init__(task_properties)

    def get_usd_model_hi_file(self, **kwargs):
        sub_key = 'usd.model-hi-file'
        return self.get(sub_key, **kwargs)

    def get_usd_surface_hi_file(self, **kwargs):
        sub_key = 'usd.surface-hi-file'
        return self.get(sub_key, **kwargs)

    def get_usd_surface_anm_hi_file(self, **kwargs):
        sub_key = 'usd.surface-anm-hi-file'
        return self.get(sub_key, **kwargs)

    def get_usd_surface_cfx_hi_file(self, **kwargs):
        sub_key = 'usd.surface-cfx-hi-file'
        return self.get(sub_key, **kwargs)

    def get_usd_work_surface_hi_file(self, **kwargs):
        sub_key = 'usd.work-surface-hi-file'
        return self.get(sub_key, **kwargs)

    def get_usd_hi_file(self, **kwargs):
        sub_key = 'usd.hi-file'
        return self.get(sub_key, **kwargs)

    def get_usd_var_file(self, var, **kwargs):
        sub_key = 'usd.{}-file'.format(var)
        return self.get(sub_key, **kwargs)

    def get_usd_var_file_(self, var_name, **kwargs):
        sub_key = 'usd.var-file'
        return self.get(sub_key, var=var_name, **kwargs)

    def get_work_usd_var_file(self, var, **kwargs):
        sub_key = 'usd.work-{}-file'.format(var)
        return self.get(sub_key, **kwargs)

    def get_usd_uv_map_file(self, **kwargs):
        sub_key = 'usd.uv_map-file'
        return self.get(sub_key, **kwargs)

    def get_usd_surface_uv_map_file(self, **kwargs):
        sub_key = 'usd.surface-uv_map-file'
        return self.get(sub_key, **kwargs)

    def get_xgen_file(self, **kwargs):
        sub_key = 'xgen.file'
        return self.get(sub_key, **kwargs)

    def get_xgen_files(self, **kwargs):
        sub_key = 'xgen.file'
        return self._get_results_(self.KEY, sub_key, **kwargs)

    def get_xgen_file_args(self, **kwargs):
        sub_key = 'xgen.file'
        return self._get_file_args_(self.KEY, sub_key, **kwargs)

    def get_xgen_grow_file(self, **kwargs):
        sub_key = 'xgen.grow-file'
        return self.get(sub_key, **kwargs)

    def get_abc_act_file(self, **kwargs):
        sub_key = 'abc.abc-hi-dyn-file'
        return self.get(sub_key, **kwargs)

    def get(self, sub_key, **kwargs):
        return self._get_result_(self.KEY, sub_key, **kwargs)


class RsvAssetLookQuery(AbsAssetQuery):
    KEY = 'looks'
    def __init__(self, task_properties):
        super(RsvAssetLookQuery, self).__init__(task_properties)

    def get(self, sub_key, **kwargs):
        return self._get_result_(self.KEY, sub_key, **kwargs)
    # usd-uv_map
    def get_model_usd_uv_map_file(self, **kwargs):
        sub_key = 'usd.model-uv_map-file'
        return self.get(sub_key, **kwargs)

    def get_surface_usd_uv_map_file(self, **kwargs):
        sub_key = 'usd.surface-uv_map-file'
        return self.get(sub_key, **kwargs)

    def get_usd_uv_map_file(self, **kwargs):
        sub_key = 'usd.uv_map-file'
        return self.get(sub_key, **kwargs)
    # usd-material
    def get_usd_look_file(self, **kwargs):
        sub_key = 'usd.look-file'
        return self.get(sub_key, **kwargs)
    # ass
    def get_ass_model_file(self, **kwargs):
        sub_key = 'ass.model-file'
        return self.get(sub_key, **kwargs)

    def get_ass_surface_file(self, **kwargs):
        sub_key = 'ass.surface-file'
        return self.get(sub_key, **kwargs)

    def get_ass_surface_anm_file(self, **kwargs):
        sub_key = 'ass.surface-anm-file'
        return self.get(sub_key, **kwargs)

    def get_ass_file(self, **kwargs):
        sub_key = 'ass.file'
        return self.get(sub_key, **kwargs)

    def get_ass_sub_file(self, look_pass, **kwargs):
        sub_key = 'ass.sub-file'
        return self.get(sub_key, look_pass=look_pass, **kwargs)

    def get_ass_app_file(self, app, **kwargs):
        sub_key = 'ass.app-file'
        return self.get(sub_key, app=app, **kwargs)

    def get_ass_app_sub_file(self, app, look_pass, **kwargs):
        sub_key = 'ass.app-sub-file'
        return self.get(sub_key, app=app, look_pass=look_pass, **kwargs)

    def get_ass_surface_anm_sub_file(self, look_pass, **kwargs):
        sub_key = 'ass.surface-anm-pass-file'
        return self.get(sub_key, look_pass=look_pass, **kwargs)

    def get_ass_work_file(self, **kwargs):
        sub_key = 'ass.work-file'
        return self.get(sub_key, **kwargs)

    def get_yml_file(self, **kwargs):
        sub_key = 'yml.file'
        return self.get(sub_key, **kwargs)

    def get_yml_surface_anm_file(self, **kwargs):
        sub_key = 'yml.surface-anm-file'
        return self.get(sub_key, **kwargs)

    def get_work_yml_file(self, **kwargs):
        sub_key = 'yml.work-file'
        return self.get(sub_key, **kwargs)
    # klf
    def get_model_klf_file(self, **kwargs):
        sub_key = 'klf.model-file'
        return self.get(sub_key, **kwargs)

    def get_surface_klf_file(self, **kwargs):
        sub_key = 'klf.surface-file'
        return self.get(sub_key, **kwargs)

    def get_klf_file(self, **kwargs):
        sub_key = 'klf.file'
        return self.get(sub_key, **kwargs)
    # json
    def get_klf_extra_file(self, **kwargs):
        sub_key = 'json.file'
        return self.get(sub_key, **kwargs)


class RsvAssetTextureQuery(AbsAssetQuery):
    KEY = 'textures.tx'
    def __init__(self, task_properties):
        super(RsvAssetTextureQuery, self).__init__(task_properties)

    def get(self, sub_key, **kwargs):
        return self._get_result_(self.KEY, sub_key, **kwargs)

    def get_src_directory(self, **kwargs):
        sub_key = 'src_dir'
        return self.get(sub_key, **kwargs)

    def get_tgt_directory(self, **kwargs):
        sub_key = 'tgt_dir'
        return self.get(sub_key, **kwargs)

    def get_work_directory(self, **kwargs):
        sub_key = 'work_dir'
        return self.get(sub_key, **kwargs)


class RsvAssetUsdQuery(AbsAssetQuery):
    KEY = 'usds'
    def __init__(self, task_properties):
        super(RsvAssetUsdQuery, self).__init__(task_properties)

    def get(self, sub_key, **kwargs):
        return self._get_result_(self.KEY, sub_key, **kwargs)

    def get_results(self, sub_key, **kwargs):
        return self._get_results_(self.KEY, sub_key, **kwargs) or []

    def get_rsv_unit(self, sub_key, **kwargs):
        return self._project__get_rsv_unit_(self.KEY, sub_key, **kwargs)

    def get_model_registry_file(self, **kwargs):
        sub_key = 'registry.model-file'
        return self.get(sub_key, **kwargs)

    def get_surface_registry_file(self, **kwargs):
        sub_key = 'registry.surface-file'
        return self.get(sub_key, **kwargs)

    def get_groom_registry_file(self, **kwargs):
        sub_key = 'registry.groom-file'
        return self.get(sub_key, **kwargs)

    def get_effect_registry_file(self, **kwargs):
        sub_key = 'registry.effect-file'
        return self.get(sub_key, **kwargs)

    def get_look_file(self, **kwargs):
        sub_key = 'look.file'
        return self.get(sub_key, **kwargs)

    def get_look_properties_file(self, **kwargs):
        sub_key = 'look.properties-file'
        return self.get(sub_key, **kwargs)

    def get_look_properties_files(self, **kwargs):
        sub_key = 'look.properties-file'
        return self.get_results(sub_key, **kwargs)

    def get_look_properties_file_dict(self, **kwargs):
        dic = {}
        sub_key = 'look.properties-file'
        rsv_unit = self.get_rsv_unit(sub_key, **kwargs)
        results = rsv_unit.get_results(
            version=kwargs['version']
        )
        for i_file_path in results:
            i_properties = rsv_unit.get_properties_by_result(i_file_path)
            i_look_passe_name = i_properties['look_pass']
            dic[i_look_passe_name] = i_file_path
        return dic

    def get_geometry_uv_map_look_file(self, **kwargs):
        sub_key = 'geometry.uv_map-file'
        return self.get(sub_key, **kwargs)

    def get_payload_file(self, **kwargs):
        sub_key = 'payload.file'
        return self.get(sub_key, **kwargs)

    def get_registry_file(self, **kwargs):
        sub_key = 'registry.file'
        return self.get(sub_key, **kwargs)
