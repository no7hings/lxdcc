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
                v = '{}/main/<camera>/<look-pass>.stats.####.json'.format(render_output_directory_path)
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
                v = '{}/main/<camera>/<look-pass>.profile.####.json'.format(render_output_directory_path)
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
                v = '{}/main/<camera>/<look-pass>/<render-pass>.####.exr'.format(render_output_directory_path)
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
            rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
                file_path
            )
            if rsv_task_properties:
                project = rsv_task_properties.get('project')
                asset = rsv_task_properties.get('asset')
                #
                rsv_asset = resolver.get_rsv_entity(
                    project=project, asset=asset
                )
                obj_opt.set_port_raw(
                    'options.asset', rsv_asset.path
                )
                #
                rsv_shots = resolver.get_rsv_entities(
                    project=project, branch='shot'
                )
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

    def __get_shot_assets(self, project, role, asset, shot_set_usd_file_path):
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
                asset
            )
        )
        if paths:
            paths = bsc_core.TextsOpt(paths).set_sort_to()
        #
        for i_location in paths:
            i_shot_asset = i_location.split('/')[-1]
            dic[i_shot_asset] = i_location
        return dic

    def __get_geometry_uv_map(self, project, role, asset):
        import lxresolver.commands as rsv_commands
        #
        dic = collections.OrderedDict()
        #
        resolver = rsv_commands.get_resolver()
        rsv_task = resolver.get_rsv_task(
            project=project,
            asset=asset,
            step='srf',
            task='surfacing'
        )
        work_geometry_uv_map_usd_file_unit = rsv_task.get_rsv_unit(
            keyword='asset-work-geometry-uv_map-usd-var-file'
        )
        work_geometry_uv_map_usd_file_path = work_geometry_uv_map_usd_file_unit.get_result(
            version='latest', extend_variants=dict(var='hi')
        )
        if work_geometry_uv_map_usd_file_path:
            dic['surface_work_latest'] = work_geometry_uv_map_usd_file_path
        #
        geometry_uv_map_usd_file_unit = rsv_task.get_rsv_unit(
            keyword='asset-geometry-usd-uv_map-file'
        )
        geometry_uv_map_usd_file_path = geometry_uv_map_usd_file_unit.get_result(
            version='latest'
        )
        if geometry_uv_map_usd_file_path:
            dic['surface_publish_latest'] = work_geometry_uv_map_usd_file_path
        return dic

    def __get_frame_range(self, shot_set_usd_file_path):
        from lxusd import usd_core
        #
        return usd_core.UsdStageOpt(shot_set_usd_file_path).get_frame_range()

    def _set_file_create_(self, project, role, asset, sequence, shot, start_frame, end_frame, shot_assets_dict, geometry_uv_maps_dict, shot_set_usd_file_path, asset_set_usd_file_path):
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

        c.set('asset.role', role)
        c.set('asset.name', asset)

        c.set('shot.sequence', sequence)
        c.set('shot.name', shot)
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

    def _set_result_create_(self, project, role, asset, sequence, shot, shot_assets_dict, geometry_uv_maps_dict, shot_set_usd_file_path):
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
                        asset_shot=shot
                    )
                )
                #
                start_frame, end_frame = self.__get_frame_range(shot_set_usd_file_path)
                ktn_dcc_objects.Scene.set_frame_range(start_frame, end_frame)
                #
                self._set_file_create_(
                    project,
                    role, asset,
                    sequence, shot, start_frame, end_frame,
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
                    shot_assets_dict = self.__get_shot_assets(
                        project, role, asset, shot_set_usd_file_path
                    )
                    geometry_uv_maps_dict = self.__get_geometry_uv_map(
                        project, role, asset
                    )
                    if shot_assets_dict:
                        obj_opt.set_port_enumerate_raw(
                            'variants.shot_asset', shot_assets_dict.keys()
                        )
                        obj_opt.set_port_enumerate_raw(
                            'variants.geometry_uv_map', geometry_uv_maps_dict.keys()
                        )
                        self._set_result_create_(
                            project,
                            role, asset,
                            sequence, shot,
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


class LxRenderer(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def _get_variable_switches_(self):
        from lxkatana import ktn_core
        print ktn_core.NGObjOpt(self._ktn_obj).get_source_objs()

    def set_reset(self):
        pass

    def _set_create_(self):
        from lxbasic import bsc_core

        from lxkatana import ktn_core
        #
        obj_opt = ktn_core.NGObjOpt(self._ktn_obj)
        search_dic = {
            'layer': 'lynxi_variants.layers',
            'quality': 'lynxi_variants.qualities',
            'camera': 'lynxi_variants.cameras',
            'look_pass': 'lynxi_variants.look_passes',
            'light_pass': 'lynxi_variants.light_passes'
        }
        variants_dic = {}
        for k, v in search_dic.items():
            i_raw = obj_opt.get_port_raw(
                v
            )
            if i_raw:
                i_variants = map(lambda x: str(x).strip(), i_raw.split(','))
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
            i_settings_name = 'settings__{}'.format(seq)
            i_settings_path = '{}/{}'.format(obj_opt.get_path(), i_settings_name)
            #
            i_settings = ktn_core.NGObjOpt._set_create_(i_settings_path, 'lx_settings')
            i_settings_opt = ktn_core.NGObjOpt(i_settings)
            i_x, i_y = x, y-(seq+1)*240
            i_settings_opt.set_position(
                i_x, i_y
            )
            obj_opt.get_send_port('input').connect(
                i_settings_opt.get_input_port('input')
            )
            for j_k, j_v in i_variants.items():
                i_settings_opt.set_port_raw(
                    variant_mapper[j_k], j_v
                )
            #
            i_renderer_name = 'renderer__{}'.format(seq)
            i_renderer_path = '{}/{}'.format(obj_opt.get_path(), i_renderer_name)
            i_renderer = ktn_core.NGObjOpt._set_create_(i_renderer_path, 'Render')
            i_renderer_opt = ktn_core.NGObjOpt(i_renderer)
            i_renderer_opt.set_port_raw(
                'passName', i_renderer_name
            )
            i_renderer_opt.set_position(
                i_x, i_y-120
            )
            i_settings_opt.get_output_port('output').connect(
                i_renderer_opt.get_input_port('input')
            )

    def _set_clear_(self):
        from lxkatana import ktn_core
        [ktn_core.NGObjOpt(i).set_delete() for i in ktn_core.NGObjOpt(self._ktn_obj).get_children()]

    def set_create(self):
        Utils.UndoStack.OpenGroup(self._ktn_obj.getName())
        try:
            self._set_clear_()
            self._set_create_()
        except Exception:
            raise
        finally:
            Utils.UndoStack.CloseGroup()

