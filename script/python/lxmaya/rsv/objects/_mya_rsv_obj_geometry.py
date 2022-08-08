# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract

from lxbasic import bsc_core
#
from lxutil import utl_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects
#
import lxmaya.fnc.exporters as mya_fnc_exporters


class UsdCmdBasic(object):
    @classmethod
    def _set_usd_export_(cls, root, location, file_path, start_frame, end_frame):
        # noinspection PyUnresolvedReferences
        import maya.mel as mel
        cmd_str = u'paMaUsdExport "{}" "{}" "{}" {} {}'.format(
            root, location, file_path, start_frame, end_frame
        )
        cmd_str += u' {} 1 0'
        utl_core.Log.set_module_result_trace(
            'usd export',
            u'file="{}", location="{}", frames="{}-{}" is started'.format(
                file_path, location, start_frame, end_frame
            )
        )
        #
        mel.eval(cmd_str)
        #
        utl_core.Log.set_module_result_trace(
            'usd export',
            u'file="{}", location="{}", frames="{}-{}" is completed'.format(
                file_path, location, start_frame, end_frame
            )
        )


class RsvDccGeometryHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_geometry_usd_export(self, version_scheme='match'):
        """
        :param version_scheme:
        :return:
        """
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep=pathsep
        )
        dcc_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if dcc_root.get_is_exists() is True:
            if workspace == 'work':
                keyword = 'asset-work-geometry-usd-var-file'
            elif workspace == 'publish':
                keyword = 'asset-geometry-usd-var-file'
            elif workspace == 'output':
                keyword = 'asset-output-geometry-usd-var-file'
            else:
                raise TypeError()
            # location_names = [i.name for i in dcc_root.get_children()]
            # use white list
            location_names = ['hi', 'shape', 'hair', 'aux']
            with utl_core.gui_progress(maximum=len(location_names)) as g_p:
                for i_location_name in location_names:
                    g_p.set_update()
                    #
                    i_geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
                        keyword=keyword
                    )
                    i_geometry_usd_var_file_path = i_geometry_usd_var_file_rsv_unit.get_result(
                        version=version, extend_variants=dict(var=i_location_name)
                    )
                    #
                    i_location = '{}/{}'.format(root, i_location_name)
                    i_sub_root_dag_path = bsc_core.DccPathDagOpt(i_location)
                    i_mya_sub_root_dag_path = i_sub_root_dag_path.set_translate_to(
                        pathsep=pathsep
                    )
                    #
                    sub_root_mya_obj = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
                    if sub_root_mya_obj.get_is_exists() is True:
                        mya_fnc_exporters.GeometryUsdExporter_(
                            file_path=i_geometry_usd_var_file_path,
                            root=i_location,
                            option=dict(
                                default_prim_path=root,
                                with_uv=True,
                                with_mesh=True,
                                use_override=False,
                                port_macth_patterns=['pg_*']
                            )
                        ).set_run()
        else:
            raise RuntimeError()

    def set_asset_geometry_uv_map_usd_export(self, version_scheme='match'):
        import lxusd.fnc.exporters as usd_fnc_exporters
        #
        step = self._rsv_scene_properties.get('step')
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        #
        if workspace == 'work':
            keyword_0 = 'asset-work-geometry-usd-var-file'
            keyword_1 = 'asset-work-geometry-uv_map-usd-file'
        elif workspace == 'publish':
            keyword_0 = 'asset-geometry-usd-var-file'
            keyword_1 = 'asset-geometry-uv_map-usd-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-geometry-usd-var-file'
            keyword_1 = 'asset-output-geometry-uv_map-usd-file'
        else:
            raise TypeError()
        #
        geometry_usd_hi_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        geometry_usd_var_file_path = geometry_usd_hi_file_rsv_unit.get_exists_result(
            version=version, extend_variants=dict(var='hi')
        )
        if geometry_usd_var_file_path:
            geometry_uv_map_usd_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            geometry_uv_map_usd_file_path = geometry_uv_map_usd_file_rsv_unit.get_result(
                version=version
            )
            usd_fnc_exporters.GeometryUvMapExporter(
                file_path=geometry_uv_map_usd_file_path,
                root=root,
                option=dict(
                    file_0=geometry_usd_var_file_path,
                    file_1=geometry_usd_var_file_path,
                    display_color=bsc_core.TextOpt(step).to_rgb(maximum=1.0)
                )
            ).set_run()

    def set_asset_geometry_abc_export(self, version_scheme='match'):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep=pathsep
        )
        dcc_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if dcc_root.get_is_exists() is True:
            if workspace == 'work':
                keyword = 'asset-work-geometry-abc-var-file'
            elif workspace == 'publish':
                keyword = 'asset-geometry-abc-var-file'
            elif workspace == 'output':
                keyword = 'asset-output-geometry-abc-var-file'
            else:
                raise TypeError()
            # location_names = [i.name for i in dcc_root.get_children()]
            # use white list
            location_names = ['hi', 'shape', 'hair', 'aux']
            with utl_core.gui_progress(maximum=len(location_names)) as g_p:
                for i_location_name in location_names:
                    g_p.set_update()
                    #
                    i_geometry_abc_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
                        keyword=keyword
                    )
                    i_geometry_usd_abc_file_path = i_geometry_abc_var_file_rsv_unit.get_result(
                        version=version, extend_variants=dict(var=i_location_name)
                    )
                    #
                    i_location = '{}/{}'.format(root, i_location_name)
                    i_sub_root_dag_path = bsc_core.DccPathDagOpt(i_location)
                    i_mya_sub_root_dag_path = i_sub_root_dag_path.set_translate_to(
                        pathsep=pathsep
                    )
                    #
                    sub_root_mya_obj = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
                    if sub_root_mya_obj.get_is_exists() is True:
                        mya_fnc_exporters.GeometryAbcExporter(
                            file_path=i_geometry_usd_abc_file_path,
                            root=i_location,
                            attribute_prefix=['pg'],
                            option={}
                        ).set_run()
        else:
            raise RuntimeError()


class RsvDccGeometryExtraHookOpt(
    utl_rsv_obj_abstract.AbsRsvObjHookOpt,
    UsdCmdBasic
):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryExtraHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_geometry_usd_export(self, version_scheme='match'):
        """
        :param version_scheme:
        :return:
        """
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep=pathsep
        )
        dcc_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if dcc_root.get_is_exists() is True:
            if workspace == 'work':
                keyword = 'asset-work-geometry-usd-var-file'
            elif workspace == 'publish':
                keyword = 'asset-geometry-usd-var-file'
            elif workspace == 'output':
                keyword = 'asset-output-geometry-usd-var-file'
            else:
                raise TypeError()
            #
            start_frame, end_frame = dcc_root.get('pg_start_frame'), dcc_root.get('pg_end_frame')
            # location_names = [i.name for i in dcc_root.get_children()]
            # use white list
            location_names = ['hi', 'shape', 'hair', 'aux']
            with utl_core.gui_progress(maximum=len(location_names)) as g_p:
                for i_location_name in location_names:
                    g_p.set_update()
                    #
                    if start_frame is not None and end_frame is not None:
                        pass
                    else:
                        pass

    def set_asset_geometry_proxy_usd_export(self):
        pass


class RsvDccShotGeometryHookOpt(
    utl_rsv_obj_abstract.AbsRsvObjHookOpt,
    UsdCmdBasic
):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_geometry_usd_export(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-shot_asset-geometry-usd-var-dir'
        elif workspace == 'output':
            keyword_0 = 'asset-output-shot_asset-geometry-usd-var-dir'
        else:
            raise TypeError()

        cache_frames = self._hook_option_opt.get('cache_shot_frames')
        start_frame, end_frame = bsc_core.TextOpt(cache_frames).to_frame_range()

        asset_shot_geometry_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )

        asset_shot_geometry_usd_directory_path = asset_shot_geometry_usd_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        self._set_shot_geometry_usd_export_(
            shot_asset, asset_shot_geometry_usd_directory_path, start_frame, end_frame
        )

    def set_asset_shot_geometry_abc_export(self):
        pass
    @classmethod
    def _set_shot_geometry_usd_export_(cls, shot_asset, directory_path, start_frame, end_frame):
        location_names = [
            'hi',
            'shape',
            # 'hair',
            'aux'
        ]
        #
        reference_dict = mya_dcc_objects.References().get_reference_dict()
        if shot_asset in reference_dict:
            obj = reference_dict[shot_asset][0]
            root = obj.get_content_obj_paths()[0]
            with utl_core.log_progress_bar(maximum=len(location_names), label='usd export') as l_p:
                for i_location_name in location_names:
                    i_location = '{}|{}:{}'.format(root, shot_asset, i_location_name)
                    if mya_dcc_objects.Node(i_location).get_is_exists() is True:
                        i_file_path = '{}/{}.usd'.format(directory_path, i_location_name)
                        cls._set_usd_export_(
                            root, i_location, i_file_path, start_frame, end_frame
                        )
                    l_p.set_update()
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    'usd export',
                    'namespace="{}" is non-exists'.format(shot_asset)
                )
            )


class RsvDccShotHairHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotHairHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_xgen_export(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        if workspace == 'publish':
            keyword = 'asset-shot_asset-component-dir'
        elif workspace == 'output':
            keyword = 'asset-output-shot_asset-component-dir'
        else:
            raise TypeError()
        #
        cache_frames = self._hook_option_opt.get('cache_shot_frames')
        start_frame, end_frame = bsc_core.TextOpt(cache_frames).to_frame_range()
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
        self._set_shot_xgen_export_(
            shot_asset, component_usd_directory_path, start_frame, end_frame
        )
    @classmethod
    def _set_xgen_export_(cls, root, directory_path, start_frame, end_frame):
        # noinspection PyUnresolvedReferences
        from pgmaya import exporters

        with utl_core.module_resulter_log(
            'xgen export',
            u'directory="{}", root="{}", frames="{}-{}"'.format(
                directory_path, root, start_frame, end_frame
            )
        ):
            e = exporters.AniGrmExporter()
            args = dict(
                master=root,
                cacheDir=directory_path,
                start_frame=start_frame,
                end_frame=end_frame
            )
            e.run(args)
    @classmethod
    def _set_shot_xgen_export_(cls, shot_asset, directory_path, start_frame, end_frame):
        reference_dict = mya_dcc_objects.References().get_reference_dict()
        if shot_asset in reference_dict:
            obj = reference_dict[shot_asset][0]
            root = obj.get_content_obj_paths()[0]
            cls._set_xgen_export_(root, directory_path, start_frame, end_frame)
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    'usd export',
                    'namespace="{}" is non-exists'.format(shot_asset)
                )
            )
