# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_texture_export(self, location=None, use_tx=False):
        import lxutil.dcc.dcc_operators as utl_dcc_operators
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-texture-src-dir'
            keyword_1 = 'asset-texture-tgt-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-texture-src-dir'
            keyword_1 = 'asset-temporary-texture-tgt-dir'
        else:
            raise RuntimeError()
        #
        with_texture_tx = self._hook_option_opt.get('with_texture_tx') or False
        #
        if with_texture_tx is True:
            pass
            # utl_dcc_operators.DccTexturesOpt(
            #     mya_dcc_objects.TextureReferences(
            #         option=dict(
            #             with_reference=False
            #         )
            #     )
            # ).set_tx_create_and_repath()
        else:
            utl_dcc_operators.DccTexturesOpt(
                mya_dcc_objects.TextureReferences(
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
        mya_fnc_exporters.TextureExporter(
            option=dict(
                directory_base=texture_src_directory_path,
                directory=texture_tgt_directory_path,
                #
                location=root,
                #
                fix_name_blank=True,
                use_tx=with_texture_tx,
                with_reference=False,
                #
                use_environ_map=True,
            )
        ).set_run()
