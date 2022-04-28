# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_texture_export(self, location, use_tx):
        import lxutil.dcc.dcc_operators as utl_dcc_operators
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-texture-src-dir'
            keyword_1 = 'asset-texture-tgt-dir'
        elif workspace == 'output':
            keyword_0 = 'asset-output-texture-src-dir'
            keyword_1 = 'asset-output-texture-tgt-dir'
        else:
            raise TypeError()
        #
        if use_tx is True:
            utl_dcc_operators.DccTexturesOpt(
                mya_dcc_objects.TextureReferences(
                    option=dict(
                        with_reference=False
                    )
                )
            ).set_tx_create_and_repath()
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
            src_dir_path=texture_src_directory_path,
            tgt_dir_path=texture_tgt_directory_path,
            root=location,
            option=dict(
                fix_name_blank=True,
                use_tx=use_tx,
                with_reference=False
            )
        ).set_run()
