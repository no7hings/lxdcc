# coding:utf-8
import six

import collections

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_configure, utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil.fnc import utl_fnc_obj_abs

import lxresolver.commands as rsv_commands

from lxutil.rsv import utl_rsv_obj_abstract


class RsvUsdAssetSetCreator(object):
    ASSET_OVERRIDE_VARIANTS = {
        ('mod', 'modeling', 'model'),
        ('grm', 'groom', 'groom'),
        ('efx', 'effects', 'effect'),
        ('rig', 'rigging', 'rig'),
        ('srf', 'surfacing', 'surface'),
    }
    SHOT_ASSET_OVERRIDE_VARIANTS = {
        ('rig', 'rigging', 'animation'),
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
    VARIANTS_MAPPER = {
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
    VARIANTS_MAPPER_0 = {
        'model_main': 'variants.asset_version.model',
        'groom_main': 'variants.asset_version.groom',
        'rig_main': 'variants.asset_version.rig',
        'effect_main': 'variants.asset_version.effect',
        'surface_main': 'variants.asset_version.surface',
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
    VARIANTS_VERSION_INDEX = {
        'model_main': -1,
        'groom_main': -1,
        'rig_main': 0,
        'effect_main': -1,
        'surface_main': -1,
    }
    def __init__(self, rsv_asset):
        self._rsv_asset = rsv_asset
    @classmethod
    def _get_shot_asset_cache_(cls, rsv_asset, rsv_shot):
        file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        if file_path:
            yml_file_path = bsc_core.StgTmpYamlMtd.get_file_path(file_path, 'shot-asset/{}'.format(rsv_asset.name))
            file_opt = bsc_core.StgFileOpt(yml_file_path)
            if file_opt.get_is_exists() is True:
                return file_opt.set_read()
            else:
                if bsc_core.SystemMtd.get_is_linux():
                    dict_ = cls._get_shot_asset_dict_(rsv_asset, rsv_shot)
                    file_opt.set_write(dict_)
                    return dict_
                return {}
        else:
            return bsc_objects.Content(value={})
    @classmethod
    def _get_shot_asset_dict_(cls, rsv_asset, rsv_shot):
        from lxusd import usd_core

        dict_ = collections.OrderedDict()

        shot_set_dress_usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        #
        # noinspection PyBroadException
        try:
            paths = usd_core.UsdStageOpt(
                shot_set_dress_usd_file_path
            ).set_obj_paths_find(
                '/assets/*/{}*'.format(
                    rsv_asset.get('asset')
                )
            )
            if paths:
                paths = bsc_core.RawTextsOpt(paths).set_sort_to()
            #
            for i_location in paths:
                i_shot_asset = i_location.split('/')[-1]
                dict_[i_shot_asset] = i_location
        except:
            utl_core.Log.set_module_error_trace(
                'shot-asset resolver',
                'file="{}" is error'.format(shot_set_dress_usd_file_path)
            )
        finally:
            return dict_
    @classmethod
    def _get_shot_asset_override_dict_(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        dict_ = collections.OrderedDict()
        shot_asset = rsv_asset.get('asset')
        asset_shot = rsv_shot.get('shot')
        #
        cur_workspace = rsv_scene_properties.get('workspace')
        cur_step = rsv_scene_properties.get('step')
        cur_task = rsv_scene_properties.get('task')
        cur_version = rsv_scene_properties.get('version')
        cur_rsv_task = rsv_asset.get_rsv_task(
            step=cur_step,
            task=cur_task
        )
        if cur_workspace == 'work':
            pass
        elif cur_workspace == 'publish':
            pass
        elif cur_workspace == 'output':
            comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
                keyword='asset-temporary-shot_asset-component-registry-usd-file'
            )
            register_usd_file_path = comp_register_usd_file_rsv_unit.get_result(
                version=cur_version,
                extend_variants=dict(
                    asset_shot=asset_shot,
                    shot_asset=shot_asset
                )
            )
            if register_usd_file_path is not None:
                dict_[shot_asset] = register_usd_file_path
        return dict_
    @classmethod
    def _get_rsv_asset_shots_(cls, rsv_asset):
        lis = []
        #
        resolver = rsv_commands.get_resolver()
        #
        rsv_shots = resolver.get_rsv_resources(
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
                    shot_assets_dict = cls._get_shot_asset_cache_(
                        rsv_asset, i_rsv_shot
                    )
                    if shot_assets_dict:
                        lis.append(i_rsv_shot)
        return lis
    @classmethod
    def _get_shot_frame_range_(cls, rsv_shot):
        from lxusd import usd_core

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
                    keyword='asset-source-asset-set-usd-file'
                )
                # debug for usd update error, auto update version
                usd_file_path = usd_file_rsv_unit.get_result(version='new')
            elif workspace in ['publish']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            elif workspace in ['output']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-temporary-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_core.StgUserMtd.get_user_temporary_directory(),
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
                    keyword='asset-source-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version='new',
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
            elif workspace in ['publish']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
            elif workspace in ['output']:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-temporary-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_core.StgUserMtd.get_user_temporary_directory(),
                rsv_asset.path
            )
        return usd_file_path
    @classmethod
    def _get_asset_usd_set_dress_variant_dict_(cls, rsv_asst):
        usd_file_path = cls._get_asset_set_dress_file_path_(rsv_asst)
        return cls._get_usd_file_variant_dict_(usd_file_path)
    @classmethod
    def _get_asset_usd_set_dress_variant_cache_(cls, rsv_asset):
        file_path = cls._get_asset_set_dress_file_path_(rsv_asset)
        if file_path:
            yml_file_path = bsc_core.StgTmpYamlMtd.get_file_path(file_path, 'asset-versions/{}'.format(rsv_asset.name))
            file_opt = bsc_core.StgFileOpt(yml_file_path)
            if file_opt.get_is_exists() is True:
                return file_opt.set_read()
            else:
                if bsc_core.SystemMtd.get_is_linux():
                    dict_ = cls._get_asset_usd_set_dress_variant_dict_(rsv_asset)
                    file_opt.set_write(dict_)
                    return dict_
                return {}
        else:
            return bsc_objects.Content(value={})
    @classmethod
    def _get_shot_usd_set_dress_variant_dict_(cls, rsv_shot):
        usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        return cls._get_usd_file_variant_dict_(usd_file_path)
    @classmethod
    def _get_usd_file_variant_dict_(cls, usd_file_path):
        from lxusd import usd_core

        c = bsc_objects.Configure(value=collections.OrderedDict())
        usd_stage_opt = usd_core.UsdStageOpt(usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        if usd_file_path:
            usd_variant_dict = usd_prim_opt.get_variant_dict()
            for i_variant_set_name, i_port_path in cls.VARIANTS_MAPPER.items():
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
    def _get_usd_variant_dict_(cls, rsv_asset, rsv_scene_properties, asset_usd_file_path):
        from lxusd import usd_core

        c = bsc_objects.Configure(value=collections.OrderedDict())
        cur_step = rsv_scene_properties.get('step')
        cur_key = cls.STEP_MAPPER[cur_step]
        usd_stage_opt = usd_core.UsdStageOpt(asset_usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()
        asset_set_dress_usd_file_path = cls._get_asset_set_dress_file_path_(rsv_asset)
        if asset_set_dress_usd_file_path:
            variants_mapper = cls.VARIANTS_MAPPER
        else:
            variants_mapper = cls.VARIANTS_MAPPER_0
        #
        for i_variant_set_name, i_port_path in variants_mapper.items():
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
                    if i_variant_set_name in cls.VARIANTS_VERSION_INDEX:
                        if i_variant_names:
                            i_current_variant_name = i_variant_names[cls.VARIANTS_VERSION_INDEX[i_variant_set_name]]
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
            i_cur_rsv_task = rsv_asset.get_rsv_task(
                step=i_step, task=i_task
            )
            if i_cur_rsv_task is not None:
                i_version_main_dict = cls._get_asset_version_main_dict_(
                    i_cur_rsv_task
                )
                configure.set(
                    'asset.version_main.{}'.format(i_key), i_version_main_dict
                )
                i_version_override_dict = cls._get_asset_version_override_dict_(
                    rsv_scene_properties,
                    i_cur_rsv_task
                )
                configure.set(
                    'asset.version_override.{}'.format(i_key), i_version_override_dict
                )
    @classmethod
    def _get_asset_version_main_dict_(cls, cur_rsv_task):
        dict_ = collections.OrderedDict()
        comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
            keyword='asset-component-registry-usd-file'
        )
        comp_register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
            version='all'
        )
        for i_file_path in comp_register_usd_file_paths:
            i_properties = comp_register_usd_file_rsv_unit.get_properties_by_result(i_file_path)
            i_version = i_properties.get('version')
            dict_[i_version] = i_file_path
        return dict_
    @classmethod
    def _get_asset_version_override_dict_(cls, rsv_scene_properties, cur_rsv_task):
        dict_ = collections.OrderedDict()
        #
        cur_workspace = rsv_scene_properties.get('workspace')
        cur_step = cur_rsv_task.get('step')
        if cur_workspace == 'work':
            if cur_step in ['srf']:
                RsvTaskOverrideUsdCreator(
                    cur_rsv_task
                )._set_geometry_uv_map_create_()
                #
                work_asset_geometry_uv_map_var_file_unit = cur_rsv_task.get_rsv_unit(
                    keyword='asset-source-geometry-uv_map-usd-var-file'
                )
                work_asset_geometry_uv_map_var_file_paths = work_asset_geometry_uv_map_var_file_unit.get_result(
                    version='all', extend_variants=dict(var='hi')
                )
                for i_file_path in work_asset_geometry_uv_map_var_file_paths:
                    i_properties = work_asset_geometry_uv_map_var_file_unit.get_properties_by_result(i_file_path)
                    i_version = i_properties.get('version')
                    dict_[i_version] = i_file_path
        elif cur_workspace == 'publish':
            comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
                keyword='asset-component-registry-usd-file'
            )
            register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
                version='all'
            )
            for i_file_path in register_usd_file_paths:
                i_properties = comp_register_usd_file_rsv_unit.get_properties_by_result(i_file_path)
                i_version = i_properties.get('version')
                dict_[i_version] = i_file_path
        elif cur_workspace == 'output':
            comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
                keyword='asset-temporary-component-registry-usd-file'
            )
            register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
                version='all'
            )
            for i_file_path in register_usd_file_paths:
                i_properties = comp_register_usd_file_rsv_unit.get_properties_by_result(i_file_path)
                i_version = i_properties.get('version')
                dict_[i_version] = i_file_path
        return dict_
    @classmethod
    def _set_asset_usd_file_create_(cls, rsv_asset, rsv_scene_properties):
        asset_set_dress_usd_file_path = cls._get_asset_set_dress_file_path_(rsv_asset)
        if asset_set_dress_usd_file_path:
            pass
        #
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
        #
        new_raw = t.render(
            c.value
        )

        bsc_core.StgFileOpt(
            asset_set_usd_file_path
        ).set_write(
            new_raw
        )
        return asset_set_usd_file_path
    @classmethod
    def _set_asset_shot_usd_file_create_(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        from lxusd import usd_core

        shot_set_dress_usd_file_path = cls._get_shot_set_dress_file_path_(rsv_shot)
        if shot_set_dress_usd_file_path:
            asset_shot_set_usd_file_path = cls._get_asset_shot_usd_file_path_(
                rsv_asset, rsv_shot,
                rsv_scene_properties
            )
            start_frame, end_frame = usd_core.UsdStageOpt(shot_set_dress_usd_file_path).get_frame_range()
            shot_asset_main_dict = cls._get_shot_asset_dict_(rsv_asset, rsv_shot)
            shot_asset_override_dict = cls._get_shot_asset_override_dict_(rsv_asset, rsv_shot, rsv_scene_properties)

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

            c.set('shot.shot_asset_main', shot_asset_main_dict)
            c.set('shot.shot_asset_override', shot_asset_override_dict)

            cls._set_asset_all_comp_registry_update_(
                c, rsv_asset, rsv_scene_properties
            )

            c.set_flatten()
            raw = t.render(
                c.value
            )

            bsc_core.StgFileOpt(
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


class RsvUsdShotSetCreator(object):
    def __init__(self, rsv_shot):
        self._rsv_shot = rsv_shot
    @classmethod
    def get_effect_component_paths(cls, usd_file_path):
        from lxusd import usd_core

        paths = usd_core.UsdStageOpt(
            usd_file_path
        ).set_obj_paths_find(
            '/assets/efx/effects/*'
        )
        if paths:
            paths = bsc_core.RawTextsOpt(paths).set_sort_to()
        return paths


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
        import lxusd.fnc.exporters as usd_fnc_exporters
        #
        root = self.get('root')
        work_asset_geometry_var_file_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-geometry-usd-var-file'
        )
        work_asset_geometry_uv_map_var_file_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-geometry-uv_map-usd-var-file'
        )
        work_asset_geometry_hi_file_paths = work_asset_geometry_var_file_unit.get_result(
            version='all', extend_variants=dict(var=var_name)
        )
        for i_work_asset_geometry_var_file_path in work_asset_geometry_hi_file_paths:
            i_properties = work_asset_geometry_var_file_unit.get_properties_by_result(i_work_asset_geometry_var_file_path)
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


class RsvUsdHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    COLOR_SCHEME = [
        'object_color',
        'group_color',
        'asset_color',
        'shell_color',
        'uv_map_color'
    ]
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvUsdHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_asset_component_usd_create(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        if workspace == 'publish':
            keyword = 'asset-shot_asset-component-usd-dir'
        elif workspace == 'output':
            keyword = 'asset-temporary-shot_asset-component-usd-dir'
        else:
            raise TypeError()
        #
        component_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        component_usd_directory_path = component_usd_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        key = 'usda/set/shot-asset'
        c = utl_configure.Jinja.get_configure(key)
        c.set_update(
            self._rsv_scene_properties.value
        )
        c.set_update(
            dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        c.set_flatten()

        usda_dict = c.get('usdas')
        #
        for k, v in usda_dict.items():
            t = utl_configure.Jinja.get_template(
                u'{}/{}'.format(key, k)
            )
            i_raw = t.render(
                **c.value
            )
            i_usda_file_path = u'{}/{}'.format(
                component_usd_directory_path, v
            )
            i_file = utl_dcc_objects.OsFile(i_usda_file_path)
            if i_file.get_is_exists() is False:
                utl_dcc_objects.OsFile(i_usda_file_path).set_write(
                    i_raw
                )

    def set_asset_shot_set_usd_create(self):
        pass

    def set_asset_user_property_usd_create(self):
        from lxusd import usd_core

        import lxusd.fnc.exporters as usd_fnc_exporters
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        asset = rsv_scene_properties.get('asset')
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == 'work':
            keyword_0 = 'asset-source-geometry-usd-var-file'
            keyword_1 = 'asset-source-geometry-user_property-usd-file'
        elif workspace == 'publish':
            keyword_0 = 'asset-geometry-usd-var-file'
            keyword_1 = 'asset-geometry-user_property-usd-file'
        elif workspace == 'output':
            keyword_0 = 'asset-temporary-geometry-usd-var-file'
            keyword_1 = 'asset-temporary-geometry-user_property-usd-file'
        else:
            raise TypeError()
        #
        var_names = ['hi', 'shape', 'hair']
        #
        s = usd_core.UsdStageOpt()
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        for i_var_name in var_names:
            i_geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version,
                extend_variants=dict(var=i_var_name)
            )
            if i_geometry_usd_var_file_path:
                s.set_sublayer_append(i_geometry_usd_var_file_path)
            else:
                utl_core.Log.set_module_warning_trace(
                    'look property create',
                    'variant="{}" is not found'.format(i_var_name)
                )
        #
        geometry_user_property_usd_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        geometry_user_property_usd_file_path = geometry_user_property_usd_file_rsv_unit.get_result(
            version=version
        )
        usd_fnc_exporters.GeometryLookPropertyExporter(
            option=dict(
                file=geometry_user_property_usd_file_path,
                location=root,
                #
                stage_src=s.usd_instance,
                #
                asset_name=asset,
                #
                color_seed=5,
                #
                with_object_color=True,
                with_group_color=True,
                with_asset_color=True,
                with_shell_color=True,
            )
        ).set_run()

    def set_asset_display_color_usd_create(self):
        from lxutil import utl_core

        from lxusd import usd_core

        import lxusd.fnc.exporters as usd_fnc_exporter
        #
        rsv_scene_properties = self._rsv_scene_properties

        asset = rsv_scene_properties.get('asset')
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == 'work':
            keyword_0 = 'asset-source-geometry-usd-var-file'
            keyword_1 = 'asset-source-geometry-extra-usd-dir'
        elif workspace == 'publish':
            keyword_0 = 'asset-geometry-usd-var-file'
            keyword_1 = 'asset-geometry-extra-usd-dir'
        elif workspace == 'output':
            keyword_0 = 'asset-temporary-geometry-usd-var-file'
            keyword_1 = 'asset-temporary-geometry-extra-usd-dir'
        else:
            raise TypeError()
        #
        var_names = ['hi', 'shape', 'hair']
        #
        s = usd_core.UsdStageOpt()
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        for i_var_name in var_names:
            i_geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version,
                extend_variants=dict(var=i_var_name)
            )
            if i_geometry_usd_var_file_path:
                s.set_sublayer_append(i_geometry_usd_var_file_path)
            else:
                utl_core.Log.set_module_warning_trace(
                    'geometry display-color create',
                    'file="{}" is not found'.format(i_geometry_usd_var_file_path)
                )
        #
        geometry_extra_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        #
        geometry_extra_usd_directory_path = geometry_extra_usd_directory_rsv_unit.get_result(
            version=version
        )

        for i_color_scheme in self.COLOR_SCHEME:
            i_file_path = '{}/{}.usd'.format(
                geometry_extra_usd_directory_path,
                i_color_scheme
            )
            usd_fnc_exporter.GeometryDisplayColorExporter(
                option=dict(
                    file=i_file_path,
                    location=root,
                    #
                    stage_src=s.usd_instance,
                    #
                    asset_name=asset,
                    #
                    color_seed=5,
                    #
                    color_scheme=i_color_scheme
                )
            ).set_run()

    def set_asset_component_usd_create(self):
        import lxutil.scripts as utl_scripts
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == 'work':
            keyword = 'asset-source-comp-usd-dir'
        elif workspace == 'publish':
            keyword = 'asset-component-usd-dir'
        elif workspace == 'output':
            keyword = 'asset-temporary-component-usd-dir'
        else:
            raise TypeError()
        #
        component_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        #
        component_usd_directory_path = component_usd_directory_rsv_unit.get_result(
            version=version
        )
        #
        step_mapper = dict(
            mod='usda/set/model',
            srf='usda/set/surface',
            rig='usda/set/rig',
            grm='usda/set/groom',
        )
        if step in step_mapper:
            key = step_mapper[step]
            #
            c = utl_configure.Jinja.get_configure(key)
            #
            c.set_update(
                self._rsv_scene_properties.value
            )
            #
            c.set_flatten()
            #
            look_pass_names = self.get_asset_exists_look_pass_names()
            c.set(
                'look.passes', look_pass_names
            )
            #
            usda_dict = c.get('usdas')
            #
            for k, v in usda_dict.items():
                if isinstance(v, six.string_types):
                    i_file_base = v
                    i_replace = False
                elif isinstance(v, dict):
                    i_file_base = v['file']
                    i_replace = v['replace']
                else:
                    raise RuntimeError()
                t = utl_configure.Jinja.get_template('{}/{}'.format(key, k))
                i_raw = t.render(
                    **c.value
                )
                i_usda_file_path = '{}/{}'.format(
                    component_usd_directory_path, i_file_base
                )
                i_file = utl_dcc_objects.OsFile(i_usda_file_path)
                if i_file.get_is_exists() is False:
                    utl_dcc_objects.OsFile(i_usda_file_path).set_write(
                        i_raw
                    )
                else:
                    if i_replace is True:
                        i_start_frame, i_end_frame = utl_scripts.DotUsdaFileReader(
                            i_usda_file_path
                        ).get_frame_range()
                        c.set('start_frame', i_start_frame)
                        c.set('end_frame', i_end_frame)
                        i_raw = t.render(
                            **c.value
                        )
                        utl_dcc_objects.OsFile(i_usda_file_path).set_write(
                            i_raw
                        )
            #
            if workspace in ['publish']:
                # noinspection PyUnresolvedReferences
                import production.gen.record_set_registry as pgs
                register_file_path = '{}/registry.usda'.format(component_usd_directory_path)
                pgs.run(register_file_path)
