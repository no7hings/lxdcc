# coding:utf-8
import collections

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_configure, utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxusd.fnc.exporters as usd_fnc_exporters

from lxutil.fnc import utl_fnc_obj_abs

import lxresolver.commands as rsv_commands

from lxusd import usd_core


class RsvAssetSetUsdCreator(object):
    ASSET_OVERRIDE_VARIANTS = {
        ('mod', 'modeling', 'model'),
        ('grm', 'groom', 'groom'),
        ('efx', 'effects', 'effect'),
        ('rig', 'rigging', 'rig'),
        ('srf', 'surfacing', 'surface'),
    }
    STEP_MAPPER = {
        'mod': 'model',
        'grm': 'groom',
        'rig': 'rig',
        'effect': 'efx',
        'srf': 'surface',
    }
    TASK_MAPPER = {
        'modeling': 'model',
        'groom': 'groom',
        'rigging': 'rig',
        'effects': 'effect',
        'surfacing': 'surface',
    }
    VARIANTS = {
        'modeling': 'variants.asset_version.model',
        'groom': 'variants.asset_version.groom',
        'rigging': 'variants.asset_version.rig',
        'effects': 'variants.asset_version.effect',
        'surfacing': 'variants.asset_version.surface',
        #
        'model_override': 'variants.asset_version_override.model',
        'groom_override': 'variants.asset_version_override.groom',
        'rig_override': 'variants.asset_version_override.rig',
        'effect_override': 'variants.asset_version_override.effect',
        'surface_override': 'variants.asset_version_override.surface',
        #
        'animation': 'variants.shot_version.animation',
        #
        'animation_override': 'variants.shot_version_override.animation',
    }
    def __init__(self, rsv_asset):
        self._rsv_asset = rsv_asset
    @classmethod
    def _get_shot_asset_dict_(cls, rsv_asset, rsv_shot):
        #
        dic = collections.OrderedDict()

        shot_set_dress_usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        #
        paths = usd_core.UsdStageOpt(
            shot_set_dress_usd_file_path
        ).set_obj_paths_find(
            '/assets/*/{}*'.format(
                rsv_asset.get('asset')
            )
        )
        if paths:
            paths = bsc_core.TextsOpt(paths).set_sort_to()
        #
        for i_location in paths:
            i_shot_asset = i_location.split('/')[-1]
            dic[i_shot_asset] = i_location
        return dic
    @classmethod
    def _get_rsv_asset_shots_(cls, rsv_asset):
        lis = []
        #
        resolver = rsv_commands.get_resolver()
        #
        rsv_shots = resolver.get_rsv_entities(
            project=rsv_asset.get('project'), branch='shot'
        )
        for i_rsv_shot in rsv_shots:
            i_rsv_shot_set_task = i_rsv_shot.get_rsv_task(
                workspace='publish', step='set', task='registry'
            )
            if i_rsv_shot_set_task is not None:
                i_rsv_shot_set_usd_file = i_rsv_shot_set_task.get_rsv_unit(
                    keyword='shot-set-dress-usd-file'
                )
                i_shot_set_usd_file_path = i_rsv_shot_set_usd_file.get_result(
                    version='latest'
                )
                if i_shot_set_usd_file_path is not None:
                    shot_assets_dict = cls._get_shot_asset_dict_(
                        rsv_asset, i_rsv_shot
                    )
                    if shot_assets_dict:
                        lis.append(i_rsv_shot)
        return lis
    @classmethod
    def _get_shot_frame_range_(cls, rsv_shot):
        shot_set_dress_usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        if shot_set_dress_usd_file_path:
            return usd_core.UsdStageOpt(
                shot_set_dress_usd_file_path
            ).get_frame_range()
    @classmethod
    def _get_asset_set_dress_file_path_(cls, rsv_asset):
        rsv_asset_set_task = rsv_asset.get_rsv_task(
            workspace='publish', step='set', task='registry'
        )
        if rsv_asset_set_task is not None:
            asset_set_dress_usd_file_rsv_unit = rsv_asset_set_task.get_rsv_unit(
                keyword='asset-set-dress-usd-file'
            )
            return asset_set_dress_usd_file_rsv_unit.get_result(
                version='latest'
            )
    @classmethod
    def _get_shot_set_dress_file_path_(cls, rsv_shot):
        rsv_shot_set_task = rsv_shot.get_rsv_task(
            workspace='publish', step='set', task='registry'
        )
        if rsv_shot_set_task is not None:
            shot_set_dress_usd_file_rsv_unit = rsv_shot_set_task.get_rsv_unit(
                keyword='shot-set-dress-usd-file'
            )
            return shot_set_dress_usd_file_rsv_unit.get_result(
                version='latest'
            )
    @classmethod
    def _get_asset_usd_file_path_(cls, rsv_asset, rsv_scene_properties):
        usd_file_path = None
        #
        if rsv_scene_properties:
            resolver = rsv_commands.get_resolver()
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)
            if workspace in ['work']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-work-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            elif workspace in ['publish']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            elif workspace in ['output']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-output-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_core.SystemMtd.get_temporary_directory_path(),
                rsv_asset.path
            )
        return usd_file_path
    @classmethod
    def _get_asset_shot_usd_file_path_(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        usd_file_path = None
        if rsv_scene_properties:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            if workspace in ['work']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-work-asset-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
            elif workspace in ['publish']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-asset-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
            elif workspace in ['output']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-output-asset-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_core.SystemMtd.get_temporary_directory_path(),
                rsv_asset.path
            )
        return usd_file_path
    @classmethod
    def _get_asset_comp_registry_(cls, rsv_scene_properties, per_rsv_task):
        dic = collections.OrderedDict()
        if per_rsv_task is not None:
            comp_register_usd_file_rsv_unit = per_rsv_task.get_rsv_unit(
                keyword='asset-comp-registry-usd-file'
            )
            register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
                version='all'
            )
            for i_file_path in register_usd_file_paths:
                i_properties = comp_register_usd_file_rsv_unit.get_properties(i_file_path)
                i_version = i_properties.get('version')
                dic[i_version] = i_file_path
        return dic
    @classmethod
    def _get_asset_comp_registry_override_(cls, rsv_scene_properties, per_rsv_task):
        workspace = rsv_scene_properties.get('workspace')
        per_step = per_rsv_task.get('step')
        dic = collections.OrderedDict()
        if per_rsv_task is not None:
            if workspace == 'work':
                if per_step in ['srf']:
                    RsvTaskOverrideUsdCreator(
                        per_rsv_task
                    )._set_geometry_uv_map_create_()
                    #
                    work_asset_geometry_uv_map_var_file_unit = per_rsv_task.get_rsv_unit(
                        keyword='asset-work-geometry-uv_map-usd-var-file'
                    )
                    work_asset_geometry_uv_map_var_file_paths = work_asset_geometry_uv_map_var_file_unit.get_result(
                        version='all', extend_variants=dict(var='hi')
                    )
                    for i_file_path in work_asset_geometry_uv_map_var_file_paths:
                        i_properties = work_asset_geometry_uv_map_var_file_unit.get_properties(i_file_path)
                        i_version = i_properties.get('version')
                        dic[i_version] = i_file_path
            elif workspace == 'publish':
                pass
            elif workspace == 'output':
                comp_register_usd_file_rsv_unit = per_rsv_task.get_rsv_unit(
                    keyword='asset-output-comp-registry-usd-file'
                )
                register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
                    version='all'
                )
                for i_file_path in register_usd_file_paths:
                    i_properties = comp_register_usd_file_rsv_unit.get_properties(i_file_path)
                    i_version = i_properties.get('version')
                    dic[i_version] = i_file_path
        return dic
    @classmethod
    def _get_asset_usd_set_dress_variant_dict_(cls, rsv_asst):
        usd_file_path = cls._get_asset_set_dress_file_path_(rsv_asst)
        return cls._get_usd_file_variant_dict_(usd_file_path)
    @classmethod
    def _get_shot_usd_set_dress_variant_dict_(cls, rsv_shot):
        usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        return cls._get_usd_file_variant_dict_(usd_file_path)
    @classmethod
    def _get_usd_file_variant_dict_(cls, usd_file_path):
        c = bsc_objects.Configure(value=collections.OrderedDict())
        usd_stage_opt = usd_core.UsdStageOpt(usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        if usd_file_path:
            usd_variant_dict = usd_prim_opt.get_variant_dict()
            for i_variant_set_name, i_port_path in cls.VARIANTS.items():
                c.set(
                    '{}.port_path'.format(i_variant_set_name),
                    i_port_path
                )
                if i_variant_set_name in usd_variant_dict:
                    i_current_variant_name, i_variant_names = usd_variant_dict[i_variant_set_name]
                    c.set(
                        '{}.variant_names'.format(i_variant_set_name),
                        i_variant_names
                    )
                    c.set(
                        '{}.variant_name'.format(i_variant_set_name),
                        i_current_variant_name
                    )
                else:
                    c.set(
                        '{}.variant_names'.format(i_variant_set_name),
                        ['None']
                    )
                    c.set(
                        '{}.variant_name'.format(i_variant_set_name),
                        'None'
                    )
        return c.value
    @classmethod
    def _get_usd_variant_dict_(cls, rsv_scene_properties, asset_usd_file_path):
        c = bsc_objects.Configure(value=collections.OrderedDict())
        cur_step = rsv_scene_properties.get('step')
        cur_key = cls.STEP_MAPPER[cur_step]
        usd_stage_opt = usd_core.UsdStageOpt(asset_usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()
        for i_variant_set_name, i_port_path in cls.VARIANTS.items():
            c.set(
                '{}.port_path'.format(i_variant_set_name),
                i_port_path
            )
            if i_variant_set_name in usd_variant_dict:
                i_current_variant_name, i_variant_names = usd_variant_dict[i_variant_set_name]
                if i_variant_names:
                    c.set(
                        '{}.variant_names'.format(i_variant_set_name),
                        i_variant_names
                    )
                    if i_variant_set_name.endswith('override'):
                        if cur_step in cls.STEP_MAPPER:
                            per_key = cls.STEP_MAPPER[cur_step]
                            if i_variant_set_name == '{}_override'.format(per_key):
                                i_current_variant_name = i_variant_names[-1]
                    else:
                        if cur_step in cls.STEP_MAPPER:
                            if i_variant_set_name in cls.TASK_MAPPER:
                                per_key = cls.TASK_MAPPER[i_variant_set_name]
                                if cur_key == per_key:
                                    i_current_variant_name = 'None'
                    #
                    c.set(
                        '{}.variant_name'.format(i_variant_set_name),
                        i_current_variant_name
                    )
            else:
                c.set(
                    '{}.variant_names'.format(
                        i_variant_set_name),
                    ['None']
                )
                c.set(
                    '{}.variant_name'.format(i_variant_set_name),
                    'None'
                )
        return c.value
    @classmethod
    def _set_asset_all_comp_registry_update_(cls, configure, rsv_asset, rsv_scene_properties):
        for i_step, i_task, i_key in cls.ASSET_OVERRIDE_VARIANTS:
            i_per_rsv_task = rsv_asset.get_rsv_task(
                step=i_step, task=i_task
            )
            if i_per_rsv_task is not None:
                i_comp_registry = cls._get_asset_comp_registry_(
                    rsv_scene_properties, i_per_rsv_task
                )
                configure.set(
                    'asset.version_main.{}'.format(i_key), i_comp_registry
                )
                i_comp_registry_override = cls._get_asset_comp_registry_override_(
                    rsv_scene_properties, i_per_rsv_task
                )
                configure.set(
                    'asset.version_override.{}'.format(i_key), i_comp_registry_override
                )
    @classmethod
    def _set_asset_usd_file_create_(cls, rsv_asset, rsv_scene_properties):
        asset_set_dress_usd_file_path = cls._get_asset_set_dress_file_path_(rsv_asset)
        if asset_set_dress_usd_file_path:
            asset_set_usd_file_path = cls._get_asset_usd_file_path_(
                rsv_asset,
                rsv_scene_properties
            )
            key = 'usda/asset-set-v002'

            t = utl_configure.Jinja.get_template(
                key
            )

            c = utl_configure.Jinja.get_configure(
                key
            )

            c.set('file', asset_set_usd_file_path)
            c.set('asset.project', rsv_asset.get('project'))
            c.set('asset.role', rsv_asset.get('role'))
            c.set('asset.name', rsv_asset.get('asset'))
            #
            c.set('asset.set_file', asset_set_dress_usd_file_path)

            cls._set_asset_all_comp_registry_update_(
                c, rsv_asset, rsv_scene_properties
            )

            c.set_flatten()
            raw = t.render(
                c.value
            )

            bsc_core.StorageFileOpt(
                asset_set_usd_file_path
            ).set_write(
                raw
            )
            return asset_set_usd_file_path
    @classmethod
    def _set_asset_shot_usd_file_create_(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        shot_set_dress_usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        if shot_set_dress_usd_file_path:
            asset_shot_set_usd_file_path = cls._get_asset_shot_usd_file_path_(
                rsv_asset, rsv_shot,
                rsv_scene_properties
            )
            start_frame, end_frame = usd_core.UsdStageOpt(shot_set_dress_usd_file_path).get_frame_range()
            shot_assets_dict = cls._get_shot_asset_dict_(rsv_asset, rsv_shot)

            key = 'usda/shot-asset-set-v002'

            t = utl_configure.Jinja.get_template(
                key
            )

            c = utl_configure.Jinja.get_configure(
                key
            )
            c.set('file', asset_shot_set_usd_file_path)
            c.set('asset.project', rsv_asset.get('project'))
            c.set('asset.role', rsv_asset.get('role'))
            c.set('asset.name', rsv_asset.get('asset'))

            c.set('shot.sequence', rsv_shot.get('sequence'))
            c.set('shot.name', rsv_shot.get('shot'))
            c.set('shot.start_frame', start_frame)
            c.set('shot.end_frame', end_frame)
            c.set('shot.set_file', shot_set_dress_usd_file_path)

            c.set('shot_assets', shot_assets_dict)

            cls._set_asset_all_comp_registry_update_(
                c, rsv_asset, rsv_scene_properties
            )

            c.set_flatten()
            raw = t.render(
                c.value
            )

            bsc_core.StorageFileOpt(
                asset_shot_set_usd_file_path
            ).set_write(
                raw
            )
            return asset_shot_set_usd_file_path

    def get_rsv_asset_shots(self):
        return self._get_rsv_asset_shots_(
            self._rsv_asset
        )

    def set_run(self):
        pass


class RsvTaskOverrideUsdCreator(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        var_names=['hi'],
        root='/master'
    )
    VAR_NAMES = ['hi']
    def __init__(self, rsv_task, option=None):
        super(RsvTaskOverrideUsdCreator, self).__init__(option)
        if rsv_task is None:
            raise TypeError()
        #
        self._rsv_task = rsv_task

    def _set_geometry_uv_map_create_at_(self, var_name):
        root = self.get('root')
        work_asset_geometry_var_file_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-geometry-usd-var-file'
        )
        work_asset_geometry_uv_map_var_file_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-geometry-uv_map-usd-var-file'
        )
        work_asset_geometry_hi_file_paths = work_asset_geometry_var_file_unit.get_result(
            version='all', extend_variants=dict(var=var_name)
        )
        for i_work_asset_geometry_var_file_path in work_asset_geometry_hi_file_paths:
            i_properties = work_asset_geometry_var_file_unit.get_properties(i_work_asset_geometry_var_file_path)
            i_version = i_properties.get('version')
            i_work_asset_geometry_uv_map_var_file_path = work_asset_geometry_uv_map_var_file_unit.get_result(
                version=i_version, extend_variants=dict(var=var_name)
            )
            if utl_dcc_objects.OsFile(i_work_asset_geometry_uv_map_var_file_path).get_is_exists() is False:
                usd_fnc_exporters.GeometryUvMapExporter(
                    file_path=i_work_asset_geometry_uv_map_var_file_path,
                    root=root,
                    option=dict(
                        file_0=i_work_asset_geometry_var_file_path,
                        file_1=i_work_asset_geometry_var_file_path
                    )
                ).set_run()

    def _set_geometry_uv_map_create_(self):
        for i_var_name in self.VAR_NAMES:
            self._set_geometry_uv_map_create_at_(i_var_name)

    def _set_geometry_display_color_create_at_(self):
        pass

    def set_run(self):
        pass
