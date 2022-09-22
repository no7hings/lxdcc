# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
from Katana import Utils, NodegraphAPI, CacheManager, RenderManager
# noinspection PyUnresolvedReferences
from UI4 import Manifest


class _MacroMtd(object):
    @classmethod
    def set_warning_show(cls, label, contents):
        from lxutil import utl_core
        #
        from lxkatana import ktn_core
        #
        if contents:
            if ktn_core._get_is_ui_mode_():
                utl_core.DialogWindow.set_create(
                    label,
                    content=u'\n'.join(contents),
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )
            else:
                for i in contents:
                    utl_core.Log.set_module_warning_trace(
                        label, i
                    )


class LxCameraAlembic(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set_port_raw(
            'alembic.file', ''
        )
        obj_opt.set_port_raw(
            'alembic.location', ''
        )
        #
        obj_opt.set_port_raw(
            'option.resolution_enable', False
        )
        obj_opt.set_port_raw(
            'option.resolution', '512x512'
        )

    def set_file_load(self):
        # adjustScreenWindow=Adjust width to match resolution
        import lxresolver.commands as rsv_commands
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_any_file_path(f)
            if rsv_task:
                rsv_entity = rsv_task.get_rsv_entity()
                rsv_camera_task = rsv_entity.get_rsv_task(
                    step='cam',
                    task='camera'
                )
                if rsv_camera_task is not None:
                    rsv_unit = rsv_camera_task.get_rsv_unit(
                        keyword='asset-camera-main-abc-file'
                    )
                    file_path = rsv_unit.get_result(version='latest')
                    if file_path:
                        obj_opt.set_port_raw(
                            'alembic.file',
                            file_path
                        )
                        obj_opt.set_port_raw(
                            'alembic.location',
                            '/root/world/cam/cameras'
                        )


class LxRenderSettings(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        pass

    def set_stats_file(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxresolver.commands as rsv_commands
        #
        import lxresolver.operators as rsv_operators
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            rsv_task_properties = rsv_commands.get_resolver().get_task_properties_by_any_scene_file_path(
                f
            )
            if rsv_task_properties:
                rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
                render_output_directory_path = rsv_asset_scene_query.get_output_render_dir()
                v = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/stats.####.json'.format(
                    render_output_directory_path)
                utl_dcc_objects.OsFile(v).set_directory_create()
                #
                obj_opt.set_port_raw(
                    'arnold_render_settings.stats_file',
                    v
                )

    def set_profile_file(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxresolver.commands as rsv_commands
        #
        import lxresolver.operators as rsv_operators
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            rsv_task_properties = rsv_commands.get_resolver().get_task_properties_by_any_scene_file_path(
                f
            )
            if rsv_task_properties:
                rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
                render_output_directory_path = rsv_asset_scene_query.get_output_render_dir()
                v = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/profile.####.json'.format(
                    render_output_directory_path)
                utl_dcc_objects.OsFile(v).set_directory_create()
                #
                obj_opt.set_port_raw(
                    'arnold_render_settings.profile_file',
                    v
                )

    def set_render_output(self):
        import lxresolver.commands as rsv_commands
        #
        import lxresolver.operators as rsv_operators
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            rsv_task_properties = rsv_commands.get_resolver().get_task_properties_by_any_scene_file_path(
                f
            )
            if rsv_task_properties:
                rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
                render_output_directory_path = rsv_asset_scene_query.get_output_render_dir()
                v = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/<render-pass>.####.exr'.format(
                    render_output_directory_path)
                #
                obj_opt.set_port_raw(
                    'lynxi_settings.render_output', v
                )


class LxAsset(object):
    VARIANTS = {
        #
        'modeling': 'usd.variants.asset_version.model',
        'groom': 'usd.variants.asset_version.groom',
        'rigging': 'usd.variants.asset_version.rig',
        'effects': 'usd.variants.asset_version.effect',
        'surfacing': 'usd.variants.asset_version.surface',
        #
        'model_override': 'usd.variants.asset_version_override.model',
        'groom_override': 'usd.variants.asset_version_override.groom',
        'rig_override': 'usd.variants.asset_version_override.rig',
        'effect_override': 'usd.variants.asset_version_override.effect',
        'surface_override': 'usd.variants.asset_version_override.surface',
        #
        'animation': 'usd.variants.shot_version.animation',
        #
        'animation_override': 'usd.variants.shot_version_override.animation',
    }
    ASSET_OVERRIDE_VARIANTS = {
        ('model', 'mod', 'modeling'),
        ('groom', 'grm', 'groom'),
        ('rig', 'rig', 'rigging'),
        ('surface', 'srf', 'surfacing'),
    }
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set(
            'options.asset', ''
        )
        obj_opt.set_as_enumerate(
            'options.shot', ['None']
        )

        obj_opt.set_port_raw(
            'usd.asset.enable', 0
        )
        obj_opt.set_port_raw(
            'usd.asset.file', ''
        )

    def set_guess(self):
        from lxutil import utl_core
        #
        import lxresolver.commands as rsv_commands
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        content = None
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        scheme = obj_opt.get('options.scheme')
        #
        rsv_asset = None
        resolver = rsv_commands.get_resolver()
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = self._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is None:
                content = 'asset="{}" is not available'.format(rsv_asset_path)
        else:
            file_path = ktn_dcc_objects.Scene.get_current_file_path()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_entity()
            else:
                content = 'file="{}" is not available'.format(file_path)

        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)
            if scheme in ['shot_asset']:
                self.__set_rsv_asset_shots_(rsv_asset)

        if content is not None:
            if ktn_core._get_is_ui_mode_():
                utl_core.DialogWindow.set_create(
                    'Shot Asset Loader',
                    content=content,
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )
    @classmethod
    def _get_rsv_asset_(cls, rsv_asset_path):
        import lxresolver.commands as rsv_commands
        #
        _ = rsv_asset_path.split('/')
        project, role, asset = _[1:]
        resolver = rsv_commands.get_resolver()
        return resolver.get_rsv_entity(
            project=project,
            asset=asset
        )
    @classmethod
    def _get_rsv_shot_(cls, rsv_shot_path):
        import lxresolver.commands as rsv_commands
        #
        _ = rsv_shot_path.split('/')
        project, sequence, shot = _[1:]
        resolver = rsv_commands.get_resolver()
        return resolver.get_rsv_entity(project=project, shot=shot)
    @classmethod
    def _get_rsv_asset_auto_(cls):
        import lxresolver.commands as rsv_commands
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if any_scene_file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_file_path(any_scene_file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_entity()
                return rsv_asset

    def _get_rsv_shot_auto_(self, rsv_asset):
        from lxkatana import ktn_core

        import lxusd.rsv.objects as usd_rsv_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        rsv_shots = usd_rsv_objects.RsvUsdAssetSetCreator._get_rsv_asset_shots_(rsv_asset)
        if rsv_shots:
            obj_opt.set_as_enumerate(
                'options.shot', [i.path for i in rsv_shots]
            )
            return rsv_shots[0]

    def __set_rsv_asset_(self, rsv_asset):
        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set(
            'options.asset', rsv_asset.path
        )

    def __set_rsv_asset_shots_(self, rsv_asset):
        from lxkatana import ktn_core

        import lxusd.rsv.objects as usd_rsv_objects

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        rsv_shots = usd_rsv_objects.RsvUsdAssetSetCreator._get_rsv_asset_shots_(rsv_asset)
        if rsv_shots:
            obj_opt.set_as_enumerate(
                'options.shot', [i.path for i in rsv_shots]
            )

    def __set_asset_usd_create_(self, rsv_asset):
        from lxkatana import ktn_core

        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        import lxusd.rsv.objects as usd_rsv_objects

        import lxresolver.commands as rsv_commands

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()

        resolver = rsv_commands.get_resolver()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            asset_set_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._set_asset_usd_file_create_(
                rsv_asset,
                rsv_scene_properties
            )
            if asset_set_usd_file_path:
                obj_opt.set_port_raw(
                    'usd.asset.enable', 1
                )
                obj_opt.set(
                    'usd.asset.file', asset_set_usd_file_path
                )
                obj_opt.set('lynxi_settings.render_start_frame', 1001.0)
                obj_opt.set('lynxi_settings.render_end_frame', 1240.0)
                obj_opt.set('lynxi_settings.render_resolution', '2048x2048')
                usd_variant_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_usd_variant_dict_(
                    rsv_asset,
                    rsv_scene_properties,
                    asset_set_usd_file_path
                )
                self.__set_usd_variant_by_dict_(usd_variant_dict)

        CacheManager.flush()

    def __set_asset_shot_usd_create_(self, rsv_asset, rsv_shot):
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        import lxusd.rsv.objects as usd_rsv_objects

        import lxresolver.commands as rsv_commands
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()

        resolver = rsv_commands.get_resolver()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            asset_shot_set_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._set_asset_shot_usd_file_create_(
                rsv_asset, rsv_shot,
                rsv_scene_properties
            )
            if asset_shot_set_usd_file_path:
                obj_opt.set_port_raw(
                    'usd.asset.enable', 1
                )
                obj_opt.set(
                    'usd.asset.file', asset_shot_set_usd_file_path
                )
                start_frame, end_frame = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_frame_range_(rsv_shot)
                obj_opt.set('lynxi_settings.render_start_frame', start_frame)
                obj_opt.set('lynxi_settings.render_end_frame', end_frame)
                #
                obj_opt.set('lynxi_settings.render_resolution', '2048x858')
                #
                shot_asset_main_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_asset_dict_(
                    rsv_asset, rsv_shot
                )
                shot_assets = [i for i in shot_asset_main_dict.keys()]
                shot_assets.append('None')
                obj_opt.set_port_enumerate_raw(
                    'usd.variants.shot_asset', shot_assets
                )
                #
                shot_asset_override_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_asset_override_dict_(
                    rsv_asset, rsv_shot, rsv_scene_properties
                )
                shot_assets_override = [i for i in shot_asset_override_dict.keys()]
                shot_assets_override.append('None')
                obj_opt.set_port_enumerate_raw(
                    'usd.variants.shot_asset_override', shot_assets_override
                )
                #
                ktn_dcc_objects.Scene.set_frame_range(start_frame, end_frame)
                #
                usd_variant_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_usd_variant_dict_(
                    rsv_asset,
                    rsv_scene_properties,
                    asset_shot_set_usd_file_path
                )
                #
                self.__set_usd_variant_by_dict_(
                    usd_variant_dict
                )
        #
        CacheManager.flush()

    def __set_asset_info_update_(self, rsv_task):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        for k, v in rsv_task.properties.value.items():
            obj_opt.set('lynxi_properties.{}'.format(k), v)

    def __set_usd_variant_by_dict_(self, dict_):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        for k, v in dict_.items():
            i_port_path = 'usd.{}'.format(v['port_path'])
            i_variant_names = v['variant_names']
            i_current_variant_name = v['variant_name']
            obj_opt.set_as_enumerate(
                i_port_path, i_variant_names
            )
            obj_opt.set(
                i_port_path,
                i_current_variant_name
            )

    def set_create(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        obj_opt.set_port_raw(
            'usd.asset.enable', 0
        )
        #
        scheme = obj_opt.get('options.scheme')
        #
        if scheme in ['asset']:
            self.__set_asset_create_()
        elif scheme in ['shot_asset']:
            self.__set_asset_shot_create_()

    def __set_asset_create_(self):
        from lxutil import utl_core
        #
        from lxkatana import ktn_core
        #
        content = None
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = self._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is None:
                content = 'asset="{}" is not available'.format(rsv_asset_path)
        else:
            rsv_asset = self._get_rsv_asset_auto_()
        #
        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)
            self.__set_asset_usd_create_(rsv_asset)
        #
        if content is not None:
            if ktn_core._get_is_ui_mode_():
                utl_core.DialogWindow.set_create(
                    'Shot Asset Loader',
                    content=content,
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )

    def __set_asset_shot_create_(self):
        from lxutil import utl_core
        #
        from lxkatana import ktn_core

        import lxusd.rsv.objects as usd_rsv_objects
        #
        content = None
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = self._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is None:
                content = 'asset="{}" is not available'.format(rsv_asset_path)
        else:
            rsv_asset = self._get_rsv_asset_auto_()

        if rsv_asset:
            self.__set_rsv_asset_(rsv_asset)
            #
            rsv_shot_path = obj_opt.get_port_raw('options.shot')
            if rsv_shot_path != 'None':
                rsv_shot = self._get_rsv_shot_(rsv_shot_path)
            else:
                rsv_shot = self._get_rsv_shot_auto_(rsv_asset)

            if rsv_asset and rsv_shot:
                shot_set_dress_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_set_dress_file_path_(
                    rsv_shot
                )
                if shot_set_dress_usd_file_path:
                    self.__set_asset_shot_usd_create_(
                        rsv_asset,
                        rsv_shot
                    )
                else:
                    content = u'shot="{}" set-dress file is non-exists'.format(rsv_shot_path)
            else:
                content = u'asset="{}" shot(s) is non-exists'.format(rsv_asset.path)
        #
        if content is not None:
            if ktn_core._get_is_ui_mode_():
                utl_core.DialogWindow.set_create(
                    'Shot Asset Loader',
                    content=content,
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )

    def set_translate_to_center(self):
        pass


class LxAssetAss(object):
    RENDER_MODE = 'previewRender'
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
    @classmethod
    def _get_input_dynamic_usd_file_(cls, rsv_asset):
        rsv_task = rsv_asset.get_rsv_task(
            step='mod', task='mod_dynamic'
        )
        if rsv_task is not None:
            keyword = 'asset-geometry-usd-var-file'
            usd_file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            return usd_file_rsv_unit.get_exists_result(version='latest', extend_variants=dict(var='hi'))
    @classmethod
    def _get_output_ass_file_(cls, rsv_scene_properties, rsv_task, look_pass_name):
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        if workspace == 'publish':
            keyword_0 = 'asset-look-ass-file'
            keyword_1 = 'asset-look-ass-sub-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-look-ass-file'
            keyword_1 = 'asset-output-look-ass-sub-file'
        else:
            raise TypeError()
        #
        if look_pass_name == 'default':
            look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
            look_ass_file_path = look_ass_file_rsv_unit.get_result(version=version)
        else:
            look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
            look_ass_file_path = look_ass_file_rsv_unit.get_result(
                version=version, extend_variants=dict(look_pass=look_pass_name)
            )
        return look_ass_file_path

    def set_guess(self):
        from lxbasic import bsc_core

        from lxusd import usd_core

        from lxkatana import ktn_core

        import lxresolver.commands as rsv_commands

        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        contents = []

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        resolver = rsv_commands.get_resolver()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)
            input_dynamic_usd_file_path = self._get_input_dynamic_usd_file_(
                rsv_task.get_rsv_entity()
            )
            if input_dynamic_usd_file_path is not None:
                guess_frame_range = usd_core.UsdStageOpt(
                    input_dynamic_usd_file_path
                ).get_frame_range()
                #
                obj_opt.set(
                    'export.scheme', 'dynamic'
                )
                obj_opt.set(
                    'export.start_frame', guess_frame_range[0]
                )
                obj_opt.set(
                    'export.end_frame', guess_frame_range[1]
                )
                obj_opt.set('export.usd.input_dynamic_file', input_dynamic_usd_file_path)
            else:
                obj_opt.set(
                    'export.scheme', 'static'
                )
            #
            scheme = obj_opt.get('export.scheme')
            #
            look_pass_name = obj_opt.get('export.look.pass')
            output_ass_file_path = self._get_output_ass_file_(
                rsv_scene_properties, rsv_task, look_pass_name
            )
            if scheme == 'static':
                obj_opt.set_expression_enable('export.ass.output_file', False)
                obj_opt.set(
                    'export.ass.output_file', output_ass_file_path
                )
            elif scheme == 'dynamic':
                output_ass_file = bsc_core.StorageFileOpt(output_ass_file_path)
                path_base = output_ass_file.path_base
                ext = output_ass_file.ext
                file_path = u'{}.%04d{}'.format(path_base, ext)
                expression = '\'{}\' % (frame)'.format(file_path)
                obj_opt.set_expression_enable('export.ass.output_file', True)
                obj_opt.set_expression('export.ass.output_file', expression)
        else:
            contents.append(
                'current scene is not available'
            )

    def set_ass_export(self):
        from lxutil import utl_core

        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        scheme = obj_opt.get('export.scheme')
        look_pass_name = obj_opt.get('export.look.pass')
        camera_path = obj_opt.get('export.camera.path')
        ass_file_path = obj_opt.get('export.ass.output_file')
        if not ass_file_path:
            return
        #
        rss = RenderManager.RenderingSettings()
        rss.ignoreROI = True
        rss.asynch = False
        rss.interactiveOutputs = True
        rss.interactiveMode = True
        #
        if not ktn_core._get_is_ui_mode_():
            Manifest.Nodes2DAPI.CreateExternalRenderListener(15900)
        #
        if scheme == 'static':
            rss.frame = ktn_core.NGObjOpt(
                NodegraphAPI.GetRootNode()
            ).get('currentTime')
            RenderManager.StartRender(
                self.RENDER_MODE,
                node=self._ktn_obj,
                views=[camera_path],
                settings=rss
            )
        elif scheme == 'dynamic':
            stat_frame, end_frame = obj_opt.get('export.start_frame'), obj_opt.get('export.end_frame')
            if stat_frame != end_frame:
                frames = range(int(stat_frame), int(end_frame)+1)
                with utl_core.log_progress_bar(maximum=len(frames), label='ass sequence export') as l_p:
                    for i_frame in frames:
                        ktn_core.NGObjOpt(
                            NodegraphAPI.GetRootNode()
                        ).set('currentTime', i_frame)
                        rss.frame = i_frame
                        RenderManager.StartRender(
                            self.RENDER_MODE,
                            node=self._ktn_obj,
                            views=[camera_path],
                            settings=rss
                        )
                        l_p.set_update()
                        utl_core.Log.set_module_result_trace(
                            'ass sequence export',
                            'look-pass="{}", frame="{}"'.format(look_pass_name, i_frame)
                        )


class LxGeometrySettings(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set('usd.location', '')
        obj_opt.set('usd.file', '')
        obj_opt.set('usd.start_frame', 1001)
        obj_opt.set('usd.end_frame', 1001)
        obj_opt.set('usd.override_enable', False)
        obj_opt.set('usd.shot_override.file', '')

    def set_usd_guess(self):
        from lxusd import usd_core

        from lxkatana import ktn_core

        contents = []

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        stage_opt = ktn_core.KtnSGStageOpt(self._ktn_obj)

        location = None
        scheme = obj_opt.get('options.scheme')
        if scheme == 'asset':
            location = '/root/world/geo/master'
        elif scheme == 'shot':
            rsv_asset = LxAsset._get_rsv_asset_auto_()
            if rsv_asset is not None:
                location = '/root/world/geo/assets/efx/{}'.format(
                    rsv_asset.get('asset')
                )
            else:
                contents.append(
                    'current scene is not available'
                )
        #
        if stage_opt.get_obj_exists(location) is True:
            obj_opt.set(
                'usd.location', location
            )
        else:
            contents.append(
                'location="{}" is not found'.format(location)
            )
        #
        guess_usd_file_path = self._get_usd_file_path_()
        if guess_usd_file_path:
            obj_opt.set(
                'usd.file', guess_usd_file_path
            )
            guess_frame_range = usd_core.UsdStageOpt(
                guess_usd_file_path
            ).get_frame_range()
            obj_opt.set(
                'usd.start_frame', guess_frame_range[0]
            )
            obj_opt.set(
                'usd.end_frame', guess_frame_range[1]
            )
        else:
            contents.append(
                'usd-file is not found'
            )

        _MacroMtd.set_warning_show(
            'look settings guess', contents
        )

    def _get_usd_file_path_(self):
        from lxkatana import ktn_core

        stage_opt = ktn_core.KtnSGStageOpt(self._ktn_obj)

        _ = stage_opt.get('/root/world/geo.info.usdOpArgs.fileName')
        if _:
            return _[0]

    def set_create(self):
        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        stage_opt = ktn_core.KtnSGStageOpt(self._ktn_obj)

        contents = []

        obj_opt.set('usd.override_enable', False)
        scheme = obj_opt.get('options.scheme')
        if scheme == 'asset':
            obj_opt.set('usd.override_enable', False)
        elif scheme == 'shot':
            location = obj_opt.get('usd.location')
            if stage_opt.get_obj_exists(location) is True:
                usd_file_path = self._set_override_usd_create_()
                obj_opt.set(
                    'usd.shot_override.file', usd_file_path
                )
            else:
                contents.append(
                    'location="{}" is not available'.format(location)
                )

        _MacroMtd.set_warning_show(
            'look settings guess', contents
        )

    def _set_override_usd_create_(self):
        from lxkatana import ktn_core

        import lxusd.scripts as us_scripts

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        file_path_src = obj_opt.get('usd.file')
        root = obj_opt.get('usd.shot_override.location')
        if root:
            location = obj_opt.get('usd.location')
            #
            return us_scripts.ShotUsdCombine(
                file_path_src, location[len(root):]
            ).set_run()


class LxCamera(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        obj_opt.set_port_raw(
            'alembic.enable', 0
        )
        obj_opt.set_port_raw(
            'alembic.file', ''
        )
        obj_opt.set_port_raw(
            'alembic.location', '/root/world/cam/cameras/main'
        )

    def set_load(self):
        from lxutil import utl_core
        #
        import lxresolver.commands as rsv_commands
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        obj_opt.set_port_raw(
            'alembic.enable',
            0
        )
        #
        contents = []
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_any_file_path(f)
            if rsv_task is not None:
                rsv_entity = rsv_task.get_rsv_entity()
                rsv_camera_task = rsv_entity.get_rsv_task(
                    step='cam',
                    task='camera'
                )
                if rsv_camera_task is not None:
                    rsv_unit = rsv_camera_task.get_rsv_unit(
                        keyword='asset-camera-main-abc-file'
                    )
                    file_path = rsv_unit.get_result(version='latest')
                    if file_path:
                        obj_opt.set_port_raw(
                            'alembic.enable',
                            1
                        )
                        #
                        obj_opt.set_port_raw(
                            'alembic.file',
                            file_path
                        )
                        obj_opt.set_port_raw(
                            'alembic.location',
                            '/root/world/cam/cameras/main'
                        )
                else:
                    contents.append(
                        u'asset="{}" camera task is non-exists'.format(rsv_entity.path)
                    )
            else:
                contents.append(
                    u'file={} is not not available'.format(f)
                )
        else:
            contents.append(
                u'file={} is not not available'.format(f)
            )

        _MacroMtd.set_warning_show(
            'camera load', contents
        )

    def set_variable_register(self):
        from lxkatana import ktn_core
        #
        camera_scheme = ktn_core.NGObjOpt(self._ktn_obj).get_port_raw(
            'lynxi_variants.camera_scheme'
        )
        key = 'camera'
        if camera_scheme in ['character']:
            values = [
                'full_body', 'upper_body', 'upper_body_35', 'upper_body_50', 'close_up',
                'add_0', 'add_1',
                'shot',
                'asset_free', 'shot_free'
            ]
            ktn_core.VariablesSetting().set_register(
                key, values
            )
        elif camera_scheme in ['prop']:
            values = [
                'full', 'half',
                'add_0', 'add_1'
                'shot',
                'asset_free', 'shot_free'
            ]
            ktn_core.VariablesSetting().set_register(
                key, values
            )


class LxRenderer(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
        #
        self._search_dic = collections.OrderedDict(
            [
                ('camera', ['lynxi_variants.camera_enable', 'lynxi_variants.cameras']),
                ('layer', ['lynxi_variants.layer_enable', 'lynxi_variants.layers']),
                ('light_pass', ['lynxi_variants.light_pass_enable', 'lynxi_variants.light_passes']),
                ('look_pass', ['lynxi_variants.look_pass_enable', 'lynxi_variants.look_passes']),
                ('quality', ['lynxi_variants.quality_enable', 'lynxi_variants.qualities']),
            ]
        )

    def _get_variable_switches_(self):
        pass

    def set_reset(self):
        pass

    def _set_create_(self):
        import collections

        from lxbasic import bsc_core

        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        variants_dic = collections.OrderedDict()
        for k, v in self._search_dic.items():
            enable_port_path, values_port_path = v
            i_raw = obj_opt.get_port_raw(
                values_port_path
            )
            if i_raw:
                i_variants = map(lambda i: str(i).strip(), i_raw.split(','))
            else:
                i_variants = []
            #
            variants_dic[k] = i_variants
        #
        variant_mapper = {
            'layer': 'lynxi_variants.layer',
            'quality': 'lynxi_variants.quality',
            'camera': 'lynxi_variants.camera',
            'look_pass': 'lynxi_variants.look_pass',
            'light_pass': 'lynxi_variants.light_pass'
        }
        combinations = bsc_core.VariablesMtd.get_all_combinations(
            variants_dic
        )
        x, y = 0, 0

        for seq, i_variants in enumerate(combinations):
            i_label = '__'.join(['{}'.format(v) for k, v in i_variants.items()])
            #
            i_settings_name = 'settings__{}'.format(i_label)
            i_settings_path = '{}/{}'.format(obj_opt.get_path(), i_settings_name)
            #
            i_settings = ktn_core.NGObjOpt._set_create_(i_settings_path, 'lx_render_settings')
            i_settings_opt = ktn_core.NGObjOpt(i_settings)
            i_x, i_y = x, y - (seq + 1) * 240
            i_settings_opt.set_position(
                i_x, i_y
            )
            i_settings_opt.set_color((.75, .5, .25))
            obj_opt.get_send_port('input').connect(
                i_settings_opt.get_input_port('input')
            )
            i_settings_opt.set_port_raw('variables.over', 1)
            for j_k, j_v in i_variants.items():
                i_settings_opt.set_port_raw(
                    variant_mapper[j_k], j_v
                )
            #
            i_renderer_name = 'renderer__{}'.format(i_label)
            i_renderer_path = '{}/{}'.format(obj_opt.get_path(), i_renderer_name)
            i_renderer = ktn_core.NGObjOpt._set_create_(i_renderer_path, 'Render')
            i_renderer_opt = ktn_core.NGObjOpt(i_renderer)
            i_renderer_opt.set_port_raw(
                'passName', i_renderer_name
            )
            i_renderer_opt.set_position(
                i_x, i_y - 120
            )
            i_renderer_opt.set_color((.5, .25, .25))
            i_settings_opt.get_output_port('output').connect(
                i_renderer_opt.get_input_port('input')
            )

    def _set_clear_(self):
        from lxkatana import ktn_core
        [ktn_core.NGObjOpt(i).set_delete() for i in ktn_core.NGObjOpt(self._ktn_obj).get_children()]

    def set_refresh(self):
        from lxkatana import ktn_core

        variants = ktn_core.VariablesSetting().get_variants()

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        for k, v in variants.items():
            if k in self._search_dic:
                enable_port_path, values_port_path = self._search_dic[k]
                if obj_opt.get_port_raw(enable_port_path) == 1:
                    obj_opt.set_port_raw(
                        values_port_path, ', '.join(v)
                    )

    def set_create(self):
        Utils.UndoStack.OpenGroup(self._ktn_obj.getName())
        try:
            self._set_clear_()
            self._set_create_()
        except Exception:
            raise
        finally:
            Utils.UndoStack.CloseGroup()

    def set_submit_to_deadline(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

        file_path = ktn_dcc_objects.Scene.get_current_file_path()

        w = utl_pnl_widgets.AssetRenderSubmitter(
            hook_option='file={}'.format(
                file_path
            )
        )
        w.set_window_show()


class LxVariant(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def _get_key_(self):
        from lxkatana import ktn_core
        return ktn_core.NGObjOpt(self._ktn_obj).get_port_raw('variableName')
    @classmethod
    def _get_item_values_(cls, ktn_obj):
        from lxkatana import ktn_core
        ktn_port = ktn_core.NGObjOpt(ktn_obj).get_port('patterns')
        return [ktn_core.NGPortOpt(i).get() for i in ktn_core.NGObjOpt(ktn_port).get_children()]

    def set_variable_register(self):
        from lxkatana import ktn_core
        key = self._get_key_()
        values = self._get_item_values_(self._ktn_obj)
        ktn_core.VariablesSetting().set_register(
            key, values
        )


class LxVariantChoose(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def _set_value_update_(self, values):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        key = 'lynxi_variants.value'
        value = obj_opt.get(key)
        obj_opt.set_as_enumerate(key, values)
        if value in values:
            obj_opt.set(
                key, value
            )

    def set_variable_value_load(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        key = obj_opt.get('lynxi_variants.key')
        source_objs = obj_opt.get_all_source_objs()
        values = []
        if source_objs:
            for i_ktn_obj in source_objs:
                i_obj_opt = ktn_core.NGObjOpt(i_ktn_obj)
                if i_obj_opt.type_name == 'VariableSwitch':
                    i_key = i_obj_opt.get('variableName')
                    if i_key == key:
                        i_values = LxVariant._get_item_values_(i_ktn_obj)
                        [values.append(j) for j in i_values if j not in values]
        #
        if values:
            self._set_value_update_(values)
        else:
            self._set_value_update_(['None'])
        return


class LxLook(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj


class LxWorkspace(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_workspace_create(self):
        from lxkatana import ktn_core
        import lxkatana.fnc.creators as ktn_fnc_creators

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        ktn_fnc_creators.LookWorkspaceCreator(
            option=dict(
                location=obj_opt.get_path()
            )
        ).set_run()

    def set_look_pass_add(self):
        pass


class LxLight(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_guess(self):
        from lxutil import utl_core
        #
        import lxresolver.commands as rsv_commands
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        content = None
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        scheme = obj_opt.get('options.scheme')
        #
        rsv_asset = None
        resolver = rsv_commands.get_resolver()
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = LxAsset._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is not None:
                pass
            else:
                content = u'asset="{}" is not available'.format(rsv_asset_path)
        else:
            file_path = ktn_dcc_objects.Scene.get_current_file_path()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_entity()
            else:
                content = u'file="{}" is not available'.format(file_path)

        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)

    def __set_rsv_asset_(self, rsv_asset):
        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set(
            'options.asset', rsv_asset.path
        )

    def set_create(self):
        pass

    def set_refresh_light_rig(self):
        from lxkatana import ktn_core

        import lxshotgun.rsv.objects as stg_rsv_objects

        contents = []

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = LxAsset._get_rsv_asset_(rsv_asset_path)
        else:
            rsv_asset = LxAsset._get_rsv_asset_auto_()
        #
        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)
            rsv_project = rsv_asset.get_rsv_project()
            name = obj_opt.get('lights.light_rig.name')
            index = obj_opt.get('lights.light_rig.index') or 0

            light_rig_rsv_assets = stg_rsv_objects.RsvStgProjectOpt(
                rsv_project
            ).get_standard_light_rig_rsv_assets()
            if light_rig_rsv_assets:
                #
                names = [i.name for i in light_rig_rsv_assets]
                obj_opt.set_as_enumerate(
                    'lights.light_rig.name',
                    names
                )
                index = max(min(int(index), len(names)-1), 0)
                if name != 'None':
                    if name in names:
                        obj_opt.set('lights.light_rig.name', name)
                    else:
                        obj_opt.set('lights.light_rig.name', names[index])
                else:
                    obj_opt.set('lights.light_rig.name', names[index])
            else:
                contents.append(
                    'light-rig(s) is not found'
                )

        _MacroMtd.set_warning_show(
            'light rig refresh', contents
        )

    def set_load_light_rig(self):
        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        asset = obj_opt.get('lights.light_rig.name')

        self._set_load_from_asset_light_rig_(asset)

    def _set_load_from_asset_light_rig_(self, light_rig_asset):
        from lxkatana import ktn_core

        contents = []

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = LxAsset._get_rsv_asset_(rsv_asset_path)
        else:
            rsv_asset = LxAsset._get_rsv_asset_auto_()
        #
        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)

            rsv_project = rsv_asset.get_rsv_project()

            light_rsv_task = rsv_project.get_rsv_task(
                asset=light_rig_asset, step='lgt', task='lighting'
            )
            if light_rsv_task:
                light_group_rsv_unit = light_rsv_task.get_rsv_unit(
                    keyword='asset-live_group-file'
                )
                light_group_file_path = light_group_rsv_unit.get_result(
                    version='latest'
                )
                if light_group_file_path:
                    obj_opt.set(
                        'lights.light_rig.live_group', light_group_file_path
                    )
                else:
                    contents.append(
                        u'light-rig="{}" file is non-exists, use default'.format(
                            light_rig_asset
                        )
                    )
            #
            # CacheManager.flush()
            self.set_live_groups_update()
        #
        _MacroMtd.set_warning_show(
            'light rig load', contents
        )

    def set_live_groups_update(self):
        from lxkatana import ktn_core

        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        children = obj_opt.get_children(include_type_names=['LiveGroup'])

        for i in children:
            i.reloadFromSource()
