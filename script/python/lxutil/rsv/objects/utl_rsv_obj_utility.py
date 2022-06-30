# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_work_scene_src_create(self):
        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        version = self._rsv_scene_properties.get('version')

        work_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-maya-scene-src-file'
        )
        work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
            version=version
        )

        mya_dcc_objects.Scene.set_file_save_to(
            work_scene_src_file_path
        )

    def set_texture_collection(self):
        from lxbasic import bsc_core

        version = self._rsv_scene_properties.get('version')

        layer = 'outsource'
        work_texture_base_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-base-dir'
        )

        work_texture_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-dir'
        )
        work_texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-src-dir'
        )
        work_texture_tx_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-tx-dir'
        )
        work_texture_configure_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-workspace-file'
        )

        work_texture_outsource_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-outsource-texture-dir'
        )

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        import lxutil.dcc.dcc_operators as utl_dcc_operators

        recycles_texture_directory_path = self._hook_option_opt.get('recycles_texture_directory')
        recycles_texture_directory_opt = bsc_core.StorageDirectoryOpt(recycles_texture_directory_path)
        recycles_texture_directory_opt.set_map_to_platform()
        #
        utl_dcc_operators.DccTexturesOpt(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_search_from(
            [
                recycles_texture_directory_opt.path
            ]
        )
        #
        utl_dcc_operators.DccTexturesOpt(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_tx_repath_to_orig()
        #
        work_texture_outsource_directory_path = work_texture_outsource_directory_rsv_unit.get_result(
            version=version
        )
        utl_dcc_operators.DccTexturesOpt(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_copy_and_repath_to(
            work_texture_outsource_directory_path
        )
