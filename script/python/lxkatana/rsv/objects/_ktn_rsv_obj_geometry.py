# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccGeometryHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_geometry_usd_export(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'work':
            keyword = 'asset-work-geometry-usd-var-file'
        elif workspace == 'publish':
            keyword = 'asset-geometry-usd-var-file'
        elif workspace == 'output':
            keyword = 'asset-output-geometry-usd-var-file'
        else:
            raise TypeError()

        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_result(
            version=version, extend_variants=dict(var='hi')
        )
        #
        geometry_uv_map_usd_source_file_path = ktn_dcc_objects.AssetWorkspace().get_geometry_uv_map_usd_source_file()
        if geometry_uv_map_usd_source_file_path:
            utl_dcc_objects.OsFile(geometry_uv_map_usd_source_file_path).set_copy_to_file(
                geometry_usd_var_file_path
            )

    def set_asset_geometry_uv_map_usd_export(self):
        from lxbasic import bsc_core
        #
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
