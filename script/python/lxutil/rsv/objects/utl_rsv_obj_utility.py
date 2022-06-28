# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_work_scene_src_create(self):
        pass

    def set_texture_collection(self):
        from lxbasic import bsc_core

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
