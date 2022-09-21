# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccLookHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccLookHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_look_ass_export(self, force=False, texture_use_environ_map=True):
        from lxutil import utl_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        from lxusd import usd_core
        #
        import lxkatana.fnc.exporters as ktn_fnc_exporters
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-look-ass-file'
            keyword_1 = 'asset-look-ass-sub-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-look-ass-file'
            keyword_1 = 'asset-output-look-ass-sub-file'
        else:
            raise TypeError()
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        look_pass_names = ktn_workspace.get_look_pass_names()
        #
        for i_look_pass_name in look_pass_names:
            if i_look_pass_name == 'default':
                i_look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
                i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(version=version)
            else:
                i_look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_1)
                i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(
                    version=version, extend_variants=dict(look_pass=i_look_pass_name)
                )
            #
            i_look_ass_file = utl_dcc_objects.OsFile(i_look_ass_file_path)
            if i_look_ass_file.get_is_exists() is False or force is True:
                i_look_pass_source_obj = ktn_workspace.get_pass_source_obj(i_look_pass_name)
                if i_look_pass_source_obj is not None:
                    ktn_fnc_exporters.LookAssExporter(
                        option=dict(
                            file=i_look_ass_file_path,
                            location=root,
                            #
                            look_pass_node=ktn_workspace.get_main_node('look_outputs'),
                            look_pass=i_look_pass_name,
                            #
                            texture_use_environ_map=texture_use_environ_map
                        )
                    ).set_run()
            else:
                utl_core.Log.set_module_warning_trace(
                    'look-ass export',
                    u'file="{}" is exists'.format(i_look_ass_file_path)
                )
        #
        model_act_cmp_usd_file_path = self.get_asset_model_act_cmp_usd_file()
        if model_act_cmp_usd_file_path is not None:
            ktn_workspace.set_dynamic_ass_export()

    def set_asset_look_klf_export(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-look-klf-file'
            keyword_1 = 'asset-look-json-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-look-klf-file'
            keyword_1 = 'asset-output-look-json-file'
        else:
            raise TypeError()
        #
        look_klf_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        look_klf_file_path = look_klf_file_rsv_unit.get_result(
            version=version
        )
        asset_workspace = ktn_dcc_objects.AssetWorkspace()
        #
        ktn_dcc_objects.Node('rootNode').get_port('variables.camera').set('asset_free')
        #
        asset_geometries = ktn_dcc_objects.Node('asset__geometries')
        if asset_geometries.get_is_exists() is True:
            asset_geometries.get_port('lynxi_variants.look').set('asset-work')
        #
        asset_workspace.set_look_klf_file_export(look_klf_file_path)
        # extra
        look_json_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        look_json_file_path = look_json_file_rsv_unit.get_result(
            version=version
        )
        asset_workspace.set_look_klf_extra_export(
            look_json_file_path
        )
