# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_texture_export(self, use_tx=False):
        import lxutil.dcc.dcc_operators as utl_dcc_operators
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        import lxkatana.fnc.exporters as ktn_fnc_exporters
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-texture-src-dir'
            keyword_1 = 'asset-texture-tgt-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-texture-src-dir'
            keyword_1 = 'asset-temporary-texture-tgt-dir'
        else:
            raise TypeError()
        #
        with_texture_tx = self._hook_option_opt.get('with_texture_tx') or False
        #
        if with_texture_tx is True:
            pass
            # utl_dcc_operators.DccTexturesOpt(
            #     ktn_dcc_objects.TextureReferences(
            #         option=dict(
            #             with_reference=False
            #         )
            #     )
            # ).set_tx_create_and_repath()
        else:
            utl_dcc_operators.DccTexturesOpt(
                ktn_dcc_objects.TextureReferences(
                    option=dict(
                        with_reference=False
                    )
                )
            ).set_tx_repath_to_orig()

        texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        texture_src_directory_path = texture_src_directory_rsv_unit.get_result(
            version=version
        )
        texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        texture_tgt_directory_path = texture_tgt_directory_tgt_unit.get_result(
            version=version
        )
        # TODO remove orig directory
        ktn_fnc_exporters.TextureExporter(
            option=dict(
                directory_base=texture_src_directory_path,
                directory=texture_tgt_directory_path,
                #
                fix_name_blank=True,
                use_tx=False,
                with_reference=False,
                use_environ_map=True,
            )
        ).set_run()

    def set_workspace_texture_lock(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        import lxutil.rsv.objects as utl_rsv_objects

        asset_workspace = ktn_dcc_objects.AssetWorkspace()
        location = asset_workspace.get_geometry_location()
        #
        texture_references = ktn_dcc_objects.TextureReferences()
        dcc_shaders = asset_workspace.get_all_dcc_geometry_shaders_by_location(location)
        dcc_objs = texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )

        texture_workspace_opt = utl_rsv_objects.RsvAssetWorkspaceTextureOpt(
            self._rsv_task
        )
        texture_workspace_opt.set_all_directories_locked(
            dcc_objs
        )
