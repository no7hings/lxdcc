# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccGeometryHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_geometry_usd_export(self, version_scheme='match'):
        """
        :param version_scheme:
        :return:
        """
        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        from lxmaya import ma_configure
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dat_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dat_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            if workspace == 'work':
                keyword = 'asset-work-geometry-usd-var-file'
            elif workspace == 'publish':
                keyword = 'asset-geometry-usd-var-file'
            elif workspace == 'output':
                keyword = 'asset-output-geometry-usd-var-file'
            else:
                raise TypeError()
            # location_names = [i.name for i in mya_root.get_children()]
            # use white list
            location_names = ['hi', 'shape', 'hair']
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
                        pathsep=ma_configure.Util.OBJ_PATHSEP
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
                                use_override=False
                            )
                        ).set_run()

    def set_geometry_uv_map_usd_export(self):
        from lxbasic import bsc_core

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

    def set_geometry_abc_export(self, version_scheme='match'):
        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        from lxmaya import ma_configure
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dat_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dat_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            if workspace == 'work':
                keyword = 'asset-work-geometry-abc-var-file'
            elif workspace == 'publish':
                keyword = 'asset-geometry-abc-var-file'
            elif workspace == 'output':
                keyword = 'asset-output-geometry-abc-var-file'
            else:
                raise TypeError()
            # location_names = [i.name for i in mya_root.get_children()]
            # use white list
            location_names = ['hi', 'shape']
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
                        pathsep=ma_configure.Util.OBJ_PATHSEP
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
