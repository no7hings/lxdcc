# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
from Katana import Utils, CacheManager


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
                v = '{}/main/<layer>/<quality>/<look-pass>/<light-pass>/<camera>/stats.####.json'.format(render_output_directory_path)
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
                v = '{}/main/<layer>/<quality>/<look-pass>/<light-pass>/<camera>/profile.####.json'.format(render_output_directory_path)
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
                v = '{}/main/<layer>/<quality>/<look-pass>/<light-pass>/<camera>/<render-pass>.####.exr'.format(render_output_directory_path)
                #
                obj_opt.set_port_raw(
                    'lynxi_settings.render_output', v
                )


class LxShotAsset(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set_port_raw(
            'options.asset', ''
        )
        obj_opt.set_port_enumerate_raw(
            'options.shot', ['None']
        )
        obj_opt.set_port_raw(
            'usd.file', ''
        )
        obj_opt.set_port_raw(
            'usd.location', ''
        )
        #
        obj_opt.set_port_enumerate_raw(
            'variants.shot_asset', ['None']
        )
        obj_opt.set_port_enumerate_raw(
            'variants.geometry_uv_map', ['None']
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
        asset_path = obj_opt.get_port_raw('options.asset')
        if asset_path:
            pass
        else:
            pass
        #
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task:
                self.__set_variants_update_(rsv_task)
                #
                rsv_asset = rsv_task.get_rsv_entity()
                #
                obj_opt.set(
                    'options.asset', rsv_asset.path
                )
                rsv_shots = self._get_shots_(rsv_asset)
                obj_opt.set_port_enumerate_raw(
                    'options.shot', [i.path for i in rsv_shots]
                )
            else:
                content = 'file="{}" is not available'.format(file_path)
        else:
            content = 'file="{}" is not available'.format(file_path)

        if content is not None:
            utl_core.DialogWindow.set_create(
                'Shot Asset Loader',
                content=content,
                status=utl_core.DialogWindow.GuiStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
    @classmethod
    def _get_shots_(cls, rsv_asset):
        import lxresolver.commands as rsv_commands
        #
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
                    keyword='shot-set-usd-file'
                )
                i_shot_set_usd_file_path = i_rsv_shot_set_usd_file.get_result(
                    version='latest'
                )
                if i_shot_set_usd_file_path is not None:
                    shot_assets_dict = cls._get_shot_assets_(
                        rsv_asset, i_shot_set_usd_file_path
                    )
                    if shot_assets_dict:
                        lis.append(i_rsv_shot)
        return lis
    @classmethod
    def _get_shot_assets_(cls, rsv_asset, shot_set_usd_file_path):
        from lxbasic import bsc_core
        #
        from lxusd import usd_core
        #
        dic = collections.OrderedDict()
        #
        paths = usd_core.UsdStageOpt(
            shot_set_usd_file_path
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
    def _get_asset_geometry_uv_map_(cls, rsv_asset):
        import lxresolver.commands as rsv_commands
        #
        dic = collections.OrderedDict()
        #
        resolver = rsv_commands.get_resolver()
        rsv_surface_task = resolver.get_rsv_task(
            project=rsv_asset.get('project'),
            asset=rsv_asset.get('asset'),
            step='srf',
            task='surfacing'
        )
        work_geometry_uv_map_usd_file_unit = rsv_surface_task.get_rsv_unit(
            keyword='asset-work-geometry-uv_map-usd-var-file'
        )
        work_geometry_uv_map_usd_file_path = work_geometry_uv_map_usd_file_unit.get_result(
            version='latest', extend_variants=dict(var='hi')
        )
        if work_geometry_uv_map_usd_file_path:
            dic['surface_work_latest'] = work_geometry_uv_map_usd_file_path
        #
        geometry_uv_map_usd_file_unit = rsv_surface_task.get_rsv_unit(
            keyword='asset-geometry-usd-uv_map-file'
        )
        geometry_uv_map_usd_file_path = geometry_uv_map_usd_file_unit.get_result(
            version='latest'
        )
        if geometry_uv_map_usd_file_path:
            dic['surface_publish_latest'] = work_geometry_uv_map_usd_file_path
        return dic
    @classmethod
    def _get_shot_frame_range_(cls, shot_set_usd_file_path):
        from lxusd import usd_core
        #
        return usd_core.UsdStageOpt(shot_set_usd_file_path).get_frame_range()
    @classmethod
    def _set_shot_usd_file_create_(cls, rsv_asset, rsv_shot, start_frame, end_frame, shot_assets_dict, geometry_uv_maps_dict, shot_set_usd_file_path, asset_set_usd_file_path):
        from lxbasic import bsc_core
        #
        from lxutil import utl_configure

        key = 'usda/shot-asset-set'

        t = utl_configure.Jinja.get_template(
            key
        )

        c = utl_configure.Jinja.get_configure(
            key
        )

        c.set('asset.role', rsv_asset.get('role'))
        c.set('asset.name', rsv_asset.get('asset'))

        c.set('shot.sequence', rsv_shot.get('sequence'))
        c.set('shot.name', rsv_shot.get('shot'))
        c.set('shot.start_frame', start_frame)
        c.set('shot.end_frame', end_frame)
        c.set('shot.set_file', shot_set_usd_file_path)

        c.set('shot_assets', shot_assets_dict)

        c.set('geometry_uv_maps', geometry_uv_maps_dict)

        raw = t.render(
            c.value
        )

        bsc_core.StorageFileOpt(
            asset_set_usd_file_path
        ).set_write(
            raw
        )

    def __set_result_create_(self, rsv_asset, rsv_shot, shot_assets_dict, geometry_uv_maps_dict, shot_set_usd_file_path):
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
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
                file_path
            )
            if rsv_task_properties:
                rsv_task = resolver.get_rsv_task(
                    **rsv_task_properties.value
                )
                shot_asset_set_usd_file = rsv_task.get_rsv_unit(
                    keyword='asset-work-shot-asset-set-usd-file'
                )
                asset_set_usd_file_path = shot_asset_set_usd_file.get_result(
                    version=rsv_task_properties.get('version'),
                    extend_variants=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
                #
                start_frame, end_frame = self._get_shot_frame_range_(shot_set_usd_file_path)
                obj_opt.set('lynxi_settings.render_start_frame', start_frame)
                obj_opt.set('lynxi_settings.render_end_frame', end_frame)
                ktn_dcc_objects.Scene.set_frame_range(start_frame, end_frame)
                #
                self._set_shot_usd_file_create_(
                    rsv_asset,
                    rsv_shot,
                    start_frame, end_frame,
                    shot_assets_dict, geometry_uv_maps_dict,
                    shot_set_usd_file_path,
                    asset_set_usd_file_path
                )
                obj_opt.set_port_raw(
                    'usd.file', asset_set_usd_file_path
                )
                obj_opt.set_port_raw(
                    'usd.location', '/root/world/geo/master'
                )
        #
        CacheManager.flush()

    def __set_variants_update_(self, rsv_task):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        for k, v in rsv_task.properties.value.items():
            obj_opt.set('lynxi_properties.{}'.format(k), v)

    def set_create(self):
        from lxutil import utl_core
        #
        import lxresolver.commands as rsv_commands
        #
        from lxkatana import ktn_core
        #
        content = None
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        asset_path = obj_opt.get_port_raw('options.asset')
        shot_path = obj_opt.get_port_raw('options.shot')
        if asset_path and shot_path != 'None':
            resolver = rsv_commands.get_resolver()
            _shot = shot_path.split('/')
            project, sequence, shot = _shot[1:]
            _asset = asset_path.split('/')
            project, role, asset = _asset[1:]
            rsv_asset = resolver.get_rsv_entity(project=project, asset=asset)
            rsv_shot = resolver.get_rsv_entity(project=project, shot=shot)
            rsv_task = rsv_shot.get_rsv_task(
                workspace='publish', step='set', task='registry'
            )
            if rsv_task is not None:
                set_usd_file = rsv_task.get_rsv_unit(
                    keyword='shot-set-usd-file'
                )
                shot_set_usd_file_path = set_usd_file.get_result(
                    version='latest'
                )
                if shot_set_usd_file_path:
                    shot_assets_dict = self._get_shot_assets_(
                        rsv_asset, shot_set_usd_file_path
                    )
                    if shot_assets_dict:
                        geometry_uv_maps_dict = self._get_asset_geometry_uv_map_(
                            rsv_asset
                        )
                        obj_opt.set_port_enumerate_raw(
                            'usd.variants.shot_asset', shot_assets_dict.keys()
                        )
                        obj_opt.set_port_enumerate_raw(
                            'usd.variants.geometry_uv_map', geometry_uv_maps_dict.keys()
                        )
                        self.__set_result_create_(
                            rsv_asset,
                            rsv_shot,
                            shot_assets_dict, geometry_uv_maps_dict,
                            shot_set_usd_file_path
                        )
                    else:
                        obj_opt.set_port_enumerate_raw(
                            'variants.shot_asset', ['None']
                        )
                        content = u'shot="{}" asset="{}" is unused'.format(shot_path, asset_path)
            else:
                content = u'shot="{}" registry task is non-exists'.format(shot_path)
        else:
            content = u'shot="{}" is not available'.format(shot_path)
        #
        if content is not None:
            utl_core.DialogWindow.set_create(
                'Shot Asset Loader',
                content=content,
                status=utl_core.DialogWindow.GuiStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )


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
            'alembic.location', ''
        )

    def set_load(self):
        # adjustScreenWindow=Adjust width to match resolution
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

    def set_variable_register(self):
        from lxkatana import ktn_core
        #
        camera_scheme = ktn_core.NGObjOpt(self._ktn_obj).get_port_raw(
            'lynxi_variants.camera_scheme'
        )
        key = 'camera'
        if camera_scheme in ['character']:
            values = ['full_body', 'upper_body', 'upper_body_35', 'upper_body_50', 'close_up', 'add_0', 'add_1', 'asset_free', 'shot', 'shot_free']
            ktn_core.VariablesSetting().set_register(
                key, values
            )
        elif camera_scheme in ['prop']:
            values = ['full', 'half', 'add_0', 'add_1', 'free', 'shot']
            ktn_core.VariablesSetting().set_register(
                key, values
            )


class LxRenderer(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
        #
        self._search_dic = collections.OrderedDict(
            [
                ('layer', ['lynxi_variants.layer_enable', 'lynxi_variants.layers']),
                ('quality', ['lynxi_variants.quality_enable', 'lynxi_variants.qualities']),
                ('camera', ['lynxi_variants.camera_enable', 'lynxi_variants.cameras']),
                ('look_pass', ['lynxi_variants.look_pass_enable', 'lynxi_variants.look_passes']),
                ('light_pass', ['lynxi_variants.light_pass_enable', 'lynxi_variants.light_passes'])
            ]
        )

    def _get_variable_switches_(self):
        from lxkatana import ktn_core
        print ktn_core.NGObjOpt(self._ktn_obj).get_source_objs()

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
            i_x, i_y = x, y-(seq+1)*240
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
                i_x, i_y-120
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
        pass


class LxVariant(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def _get_key_(self):
        from lxkatana import ktn_core
        return ktn_core.NGObjOpt(self._ktn_obj).get_port_raw('variableName')

    def _get_values_(self):
        from lxkatana import ktn_core
        ktn_port = ktn_core.NGObjOpt(self._ktn_obj).get_port('patterns')
        return [ktn_core.NGPortOpt(i).get() for i in ktn_core.NGObjOpt(ktn_port).get_children()]

    def set_variable_register(self):
        from lxkatana import ktn_core
        key = self._get_key_()
        values = self._get_values_()
        ktn_core.VariablesSetting().set_register(
            key, values
        )


class LxAsset(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

        obj_opt.set_port_raw(
            'option.asset', ''
        )
        obj_opt.set_port_raw(
            'option.scheme', 'asset'
        )
        obj_opt.set_port_raw(
            'usd.file', ''
        )
        obj_opt.set_port_raw(
            'usd.location', '/root/world/geo'
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
        asset_path = obj_opt.get_port_raw('options.asset')
        if asset_path:
            pass
        else:
            pass
        #
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_entity()
                obj_opt.set(
                    'options.asset', rsv_asset.path
                )
            else:
                content = 'file="{}" is not available'.format(file_path)
        else:
            content = 'file="{}" is not available'.format(file_path)

        if content is not None:
            utl_core.DialogWindow.set_create(
                'Shot Asset Loader',
                content=content,
                status=utl_core.DialogWindow.GuiStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )

    def _set_work_file_create_(self, rsv_entity, rsv_task, file_path, file_properties):
        from lxbasic import bsc_core

        from lxutil import utl_configure

        key = 'usda/work-asset-set'

        t = utl_configure.Jinja.get_template(
            key
        )

        c = utl_configure.Jinja.get_configure(
            key
        )

        c.set('file', file_path)
        c.set('properties', file_properties.value)

        layers = []
        task_args = [
            ('srf', 'surfacing'),
            ('grm', 'groom'),
            ('efx', 'effects'),
            ('mod', 'modeling'),
        ]
        for i_step, i_task in task_args:
            i_rsv_task = rsv_entity.get_rsv_task(step=i_step, task=i_task)
            if i_rsv_task is not None:
                i_usd_registry_file_unit = i_rsv_task.get_rsv_unit(
                    keyword='asset-usd-registry-file'
                )
                i_usd_registry_file_path = i_usd_registry_file_unit.get_result(
                    version='latest'
                )
                if i_usd_registry_file_path:
                    layers.append(i_usd_registry_file_path)

        c.set('layers', layers)

        raw = t.render(
            c.value
        )
        bsc_core.StorageFileOpt(
            file_path
        ).set_write(
            raw
        )

    def _set_render_file_create_(self, rsv_entity, rsv_task, file_path, file_properties):
        from lxbasic import bsc_core

        from lxutil import utl_configure

        key = 'usda/work-asset-set'

        t = utl_configure.Jinja.get_template(
            key
        )

        c = utl_configure.Jinja.get_configure(
            key
        )

        c.set('file', file_path)
        c.set('properties', file_properties.value)

        layers = []
        task_args = [
            ('srf', 'surfacing'),
            ('mod', 'modeling'),
            ('grm', 'groom'),
            ('efx', 'effects'),
        ]
        for i_step, i_task in task_args:
            i_rsv_task = rsv_entity.get_rsv_task(step=i_step, task=i_task)
            if i_rsv_task is not None:
                i_usd_registry_file_unit = i_rsv_task.get_rsv_unit(
                    keyword='asset-usd-registry-file'
                )
                i_usd_registry_file_path = i_usd_registry_file_unit.get_result(
                    version='latest'
                )
                if i_usd_registry_file_path:
                    layers.append(i_usd_registry_file_path)

        c.set('layers', layers)

        raw = t.render(
            c.value
        )
        bsc_core.StorageFileOpt(
            file_path
        ).set_write(
            raw
        )

    def __set_variants_update_(self, rsv_task):
        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        for k, v in rsv_task.properties.value.items():
            obj_opt.set('lynxi_properties.{}'.format(k), v)

    def set_create(self):
        import lxresolver.commands as rsv_commands
        #
        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        #
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        if file_path:
            resolver = rsv_commands.get_resolver()
            rsv_task = resolver.get_rsv_task_by_file_path(file_path)
            if rsv_task is not None:
                self.__set_variants_update_(rsv_task)
                #
                rsv_entity = rsv_task.get_rsv_entity()
                scheme = obj_opt.get_port_raw('options.scheme')
                if scheme in ['asset-work']:
                    work_katana_scene_src_file_unit = rsv_task.get_rsv_unit(
                        keyword='asset-work-katana-scene-src-file'
                    )
                    file_properties = work_katana_scene_src_file_unit.get_properties(
                        file_path
                    )
                    if file_properties:
                        version = file_properties.get('version')
                        work_set_usd_file_unit = rsv_task.get_rsv_unit(
                            keyword='asset-work-set-usd-file'
                        )
                        work_set_usd_file_path = work_set_usd_file_unit.get_result(version=version)

                        self._set_work_file_create_(rsv_entity, rsv_task, work_set_usd_file_path, file_properties)

                        obj_opt.set_port_raw(
                            'usd.file', work_set_usd_file_path
                        )
                if scheme in ['asset']:
                    render_katana_scene_file_unit = rsv_task.get_rsv_unit(
                        keyword='asset-render-katana-scene-file'
                    )
                    file_properties = render_katana_scene_file_unit.get_properties(
                        file_path
                    )
                    if file_properties:
                        version = file_properties.get('version')
                        render_set_usd_file_unit = rsv_task.get_rsv_unit(
                            keyword='asset-render-set-usd-file'
                        )
                        render_set_usd_file_path = render_set_usd_file_unit.get_result(version=version)
                        self._set_render_file_create_(rsv_entity, rsv_task, render_set_usd_file_path, file_properties)
                        obj_opt.set_port_raw(
                            'usd.file', render_set_usd_file_path
                        )


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
