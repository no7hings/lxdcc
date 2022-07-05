# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvRecyclerHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvRecyclerHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_texture_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        directory_path_src = self._hook_option_opt.get('recycles_texture_directory')
        if directory_path_src:
            directory_path_opt_src = bsc_core.StorageDirectoryOpt(directory_path_src)
            if directory_path_opt_src.get_is_exists() is True:
                version = self._rsv_scene_properties.get('version')

                directory_tgt_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword='asset-work-outsource-texture-dir'
                )
                directory_path_tgt = directory_tgt_rsv_unit.get_result(
                    version=version
                )

                directory_path_opt_src.set_copy_to_directory(
                    directory_path_tgt
                )

                utl_core.Log.set_module_result_trace(
                    'asset recycles',
                    u'directory="{}"'.format(
                        directory_path_tgt
                    )
                )

            else:
                utl_core.Log.set_module_warning_trace(
                    'asset recycles',
                    u'directory="{}" is non-exists'.format(
                        directory_path_src
                    )
                )

    def set_maya_file_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        from lxmaya import ma_core

        ma_core.set_stack_trace_enable(True)

        keyword = 'asset-work-maya-scene-src-file'
        file_path_src = self._hook_option_opt.get('recycles_maya_file')
        if file_path_src:
            file_path_opt_src = bsc_core.StorageFileOpt(file_path_src)
            if file_path_opt_src.get_is_exists() is True:
                version = self._rsv_scene_properties.get('version')

                file_tgt_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword
                )
                file_path_tgt = file_tgt_rsv_unit.get_result(
                    version=version
                )

                file_path_opt_src.set_copy_to_file(
                    file_path_tgt
                )

                utl_core.Log.set_module_result_trace(
                    'asset recycles',
                    u'file="{}" '.format(
                        file_path_tgt
                    )
                )

                repath_maya_texture_enable = self._hook_option_opt.get('repath_maya_texture_enable')
                if repath_maya_texture_enable is True:
                    mya_dcc_objects.Scene.set_file_open(file_path_tgt)

                    self.set_maya_texture_repath()

                    mya_dcc_objects.Scene.set_file_save()
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset recycles',
                    u'file="{}" is non-exists'.format(
                        file_path_src
                    )
                )

    def set_maya_texture_repath(self):
        import lxutil.dcc.dcc_operators as utl_dcc_operators

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        from lxbasic import bsc_core

        from lxutil import utl_core

        from lxmaya import ma_core

        ma_core.set_stack_trace_enable(True)

        version = self._rsv_scene_properties.get('version')

        work_texture_outsource_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-outsource-texture-dir'
        )

        work_texture_outsource_directory_path = work_texture_outsource_directory_rsv_unit.get_result(
            version=version
        )
        if bsc_core.StorageDirectoryOpt(work_texture_outsource_directory_path).get_is_exists() is False:
            work_texture_outsource_directory_path_0 = work_texture_outsource_directory_rsv_unit.get_exists_result(
                version='latest'
            )
            utl_core.Log.set_module_warning_trace(
                'asset recycles',
                u'directory="{}" is not found, use "{}" instance'.format(
                    work_texture_outsource_directory_path, work_texture_outsource_directory_path_0

                )
            )
            work_texture_outsource_directory_path = work_texture_outsource_directory_path_0
        #
        utl_dcc_operators.DccTexturesOpt(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_search_from(
            [
                work_texture_outsource_directory_path
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

    def set_sp_file_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        keyword = 'asset-work-sp-scene-src-file'
        file_path_src = self._hook_option_opt.get('recycles_sp_file')
        if file_path_src:
            file_path_opt_src = bsc_core.StorageFileOpt(file_path_src)
            if file_path_opt_src.get_is_exists() is True:
                version = self._rsv_scene_properties.get('version')

                file_tgt_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword
                )
                file_path_tgt = file_tgt_rsv_unit.get_result(
                    version=version
                )

                file_path_opt_src.set_copy_to_file(
                    file_path_tgt
                )

                utl_core.Log.set_module_result_trace(
                    'asset recycles',
                    u'file="{}" '.format(
                        file_path_tgt
                    )
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset recycles',
                    u'file="{}" is non-exists'.format(
                        file_path_src
                    )
                )
