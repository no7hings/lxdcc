# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvRecyclerHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvRecyclerHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_texture_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        directory_paths_src = self._hook_option_opt.get_as_array('recycles_texture_directories')
        if directory_paths_src:
            keyword = 'asset-work-texture-dir'

            variant = 'outsource'
            version = self._rsv_scene_properties.get('version')
            #
            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, extend_variants=dict(variant=variant)
            )

            directory_path_src = directory_paths_src[0]

            directory_path_opt_src = bsc_core.StorageDirectoryOpt(directory_path_src)
            directory_path_opt_src.set_map_to_platform()
            if directory_path_opt_src.get_is_exists() is True:
                directory_path_opt_src.set_copy_to_directory(
                    directory_path_tgt
                )
                utl_core.Log.set_module_result_trace(
                    'asset texture recycles',
                    u'directory="{}" >> directory="{}"'.format(
                        directory_path_src, directory_path_tgt
                    )
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset texture recycles',
                    u'directory="{}" is non-exists'.format(
                        directory_path_src
                    )
                )

    def set_maya_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        import lxutil.fnc.exporters as utl_fnc_exporters

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        from lxmaya import ma_core

        ma_core.set_stack_trace_enable(True)

        keyword_0 = 'asset-work-maya-scene-src-file'
        file_paths_src = self._hook_option_opt.get_as_array('recycles_maya_files')
        if file_paths_src:
            file_path_src = file_paths_src[0]
            file_path_opt_src = bsc_core.StorageFileOpt(file_path_src)
            file_path_opt_src.set_map_to_platform()
            if file_path_opt_src.get_is_exists() is True:
                version = self._rsv_scene_properties.get('version')

                file_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                    keyword=keyword_0
                )
                file_path_tgt = file_rsv_unit_tgt.get_result(
                    version=version
                )

                utl_fnc_exporters.DotMaExporter(
                    option=dict(
                        file_path_src=file_path_src,
                        file_path_tgt=file_path_tgt
                    )
                ).set_run()

                utl_core.Log.set_module_result_trace(
                    'asset maya recycles',
                    u'file="{}" '.format(
                        file_path_tgt
                    )
                )
                # repath texture first
                repath_maya_texture_enable = self._hook_option_opt.get_as_boolean('repath_maya_texture_enable')
                if repath_maya_texture_enable is True:
                    mya_dcc_objects.Scene.set_file_open(file_path_tgt)
                    self.set_maya_texture_repath()
                    mya_dcc_objects.Scene.set_file_save()
                # repath xgen last
                repath_maya_xgen_enable = self._hook_option_opt.get_as_boolean('repath_maya_xgen_enable')
                if repath_maya_xgen_enable is True:
                    self.set_maya_xgen_repath()
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset maya recycles',
                    u'file="{}" is non-exists'.format(
                        file_path_src
                    )
                )

    def set_xgen_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        from lxmaya import ma_core

        ma_core.set_stack_trace_enable(True)

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        keyword = 'asset-work-maya-xgen-cache-dir'

        directory_paths_src = self._hook_option_opt.get_as_array('recycles_xgen_cache_directories')
        if directory_paths_src:
            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, extend_variants=dict(variant=variant)
            )
            #
            directory_path_src = directory_paths_src[0]
            directory_path_opt_src = bsc_core.StorageDirectoryOpt(directory_path_src)
            directory_path_opt_src.set_map_to_platform()
            if directory_path_opt_src.get_is_exists() is True:
                directory_path_opt_src.set_copy_to_directory(
                    directory_path_tgt
                )
                utl_core.Log.set_module_result_trace(
                    'asset xgen cache recycles',
                    u'directory="{}" >> directory="{}"'.format(
                        directory_path_src, directory_path_tgt
                    )
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'asset xgen cache recycles',
                    u'directory="{}" is non-exists'.format(
                        directory_path_src
                    )
                )

    def set_sp_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        keyword = 'asset-work-sp-scene-src-dir'
        file_paths_src = self._hook_option_opt.get_as_array('recycles_sp_files')
        if file_paths_src:
            variant = 'outsource'
            version = self._rsv_scene_properties.get('version')

            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, extend_variants=dict(variant=variant)
            )
            for i_file_path_src in file_paths_src:
                i_file_path_opt_src = bsc_core.StorageFileOpt(i_file_path_src)
                i_file_path_opt_src.set_map_to_platform()
                if i_file_path_opt_src.get_is_exists() is True:
                    i_file_path_opt_src.set_copy_to_directory(
                        directory_path_tgt
                    )
                    utl_core.Log.set_module_result_trace(
                        'asset sp recycles',
                        u'file="{}" >> directory="{}"'.format(
                            i_file_path_opt_src, directory_path_tgt
                        )
                    )
                else:
                    utl_core.Log.set_module_warning_trace(
                        'asset sp recycles',
                        u'file="{}" is non-exists'.format(
                            i_file_path_src
                        )
                    )

    def set_zb_recycles(self):
        from lxbasic import bsc_core

        from lxutil import utl_core

        keyword = 'asset-work-zb-scene-src-dir'
        file_paths_src = self._hook_option_opt.get_as_array('recycles_zb_files')
        if file_paths_src:
            variant = 'outsource'
            version = self._rsv_scene_properties.get('version')

            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, extend_variants=dict(variant=variant)
            )
            for i_file_path_src in file_paths_src:
                i_file_path_opt_src = bsc_core.StorageFileOpt(i_file_path_src)
                # map path to current platform first
                i_file_path_opt_src.set_map_to_platform()
                if i_file_path_opt_src.get_is_exists() is True:
                    i_file_path_opt_src.set_copy_to_directory(
                        directory_path_tgt
                    )
                    utl_core.Log.set_module_result_trace(
                        'asset zb recycles',
                        u'file="{}" >> directory="{}"'.format(
                            i_file_path_opt_src, directory_path_tgt
                        )
                    )
                else:
                    utl_core.Log.set_module_warning_trace(
                        'asset zb recycles',
                        u'file="{}" is non-exists'.format(
                            i_file_path_src
                        )
                    )

    def set_maya_xgen_repath(self):
        import lxutil.dcc.dcc_operators as utl_dcc_operators

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        import lxutil.fnc.exporters as utl_fnc_exporters

        from lxbasic import bsc_core

        from lxutil import utl_core

        from lxmaya import ma_core

        ma_core.set_stack_trace_enable(True)

        keyword_0 = 'asset-work-maya-xgen-cache-dir'
        keyword_1 = 'asset-work-maya-scene-src-dir'
        keyword_2 = 'asset-work-maya-scene-src-file'

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        xgen_collection_directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        xgen_collection_directory_path_tgt = xgen_collection_directory_rsv_unit_tgt.get_result(
            version=version, extend_variants=dict(variant=variant)
        )

        xgen_project_directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        xgen_project_directory_path_tgt = xgen_project_directory_rsv_unit_tgt.get_result(
            version='latest'
        )

        maya_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_2
        )
        maya_scene_file_path = maya_scene_file_rsv_unit.get_result(
            version=version
        )

        if bsc_core.StorageDirectoryOpt(xgen_collection_directory_path_tgt).get_is_exists() is False:
            directory_path_0 = xgen_collection_directory_rsv_unit_tgt.get_exists_result(
                version='latest', extend_variants=dict(variant=variant)
            )
            utl_core.Log.set_module_warning_trace(
                'asset xgen repath',
                u'directory="{}" is not found, use "{}" instance'.format(
                    xgen_collection_directory_path_tgt, directory_path_0

                )
            )
            xgen_collection_directory_path_tgt = directory_path_0

        e = utl_fnc_exporters.DotXgenExporter

        xgen_collection_file_paths = e._get_xgen_collection_file_paths_(
            maya_scene_file_path
        )
        for i_xgen_collection_file_path in xgen_collection_file_paths:
            i_xgen_collection_name = e._get_xgen_collection_name_(i_xgen_collection_file_path)

            e._set_xgen_collection_file_repath_(
                i_xgen_collection_file_path,
                xgen_project_directory_path_tgt,
                '{}/collections'.format(xgen_collection_directory_path_tgt),
                i_xgen_collection_name,
            )

    def set_maya_texture_repath(self):
        import lxutil.dcc.dcc_operators as utl_dcc_operators

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        from lxbasic import bsc_core

        from lxutil import utl_core

        from lxmaya import ma_core

        ma_core.set_stack_trace_enable(True)

        keyword = 'asset-work-texture-dir'

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )

        directory_path_tgt = directory_rsv_unit_tgt.get_result(
            version=version, extend_variants=dict(variant=variant)
        )
        if bsc_core.StorageDirectoryOpt(directory_path_tgt).get_is_exists() is False:
            directory_path_0 = directory_rsv_unit_tgt.get_exists_result(
                version='latest', extend_variants=dict(variant=variant)
            )
            utl_core.Log.set_module_warning_trace(
                'asset texture repath',
                u'directory="{}" is not found, use "{}" instance'.format(
                    directory_path_tgt, directory_path_0

                )
            )
            directory_path_tgt = directory_path_0
        #
        utl_dcc_operators.DccTexturesOpt(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_search_from(
            [
                directory_path_tgt
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
