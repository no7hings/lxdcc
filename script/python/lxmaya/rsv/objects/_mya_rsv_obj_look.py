# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccLookHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccLookHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_look_ass_export(self, force=False, texture_use_environ_map=True):
        from lxbasic import bsc_core

        from lxutil import utl_core

        import lxutil.dcc.dcc_objects as utl_dcc_objects

        import lxmaya.fnc.exporters as mya_fnc_exporters

        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        force = False

        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')

        if workspace == 'publish':
            keyword_0 = 'asset-look-ass-file'
            keyword_1 = 'asset-look-ass-sub-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-look-ass-file'
            keyword_1 = 'asset-output-look-ass-sub-file'
        else:
            raise TypeError()
        #
        root_dag_opt = bsc_core.DccPathDagOpt(root)
        mya_root_dag_opt = root_dag_opt.set_translate_to(pathsep)
        mya_root = mya_dcc_objects.Group(mya_root_dag_opt.value)
        if mya_root.get_is_exists() is True:
            look_pass_names = self.get_asset_exists_look_pass_names()
            if look_pass_names is not None:
                look_pass_names = look_pass_names
            else:
                look_pass_names = ['default']
            # sequence-file(s) export per frame
            start_frame, end_frame = (
                mya_root.get_port('pg_start_frame').get(),
                mya_root.get_port('pg_end_frame').get()
            )
            # export per look-pass
            for i_look_pass_name in look_pass_names:
                if i_look_pass_name == 'default':
                    i_look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
                    i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(version=version)
                else:
                    i_look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_1)
                    i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(
                        version=version, extend_variants=dict(look_pass=i_look_pass_name)
                    )
                # main-file(s)
                i_look_ass_file = utl_dcc_objects.OsFile(i_look_ass_file_path)
                if i_look_ass_file.get_is_exists() is False or force is True:
                    mya_fnc_exporters.LookAssExporter(
                        option=dict(
                            file=i_look_ass_file_path,
                            location=root,
                            texture_use_environ_map=texture_use_environ_map,
                        )
                    ).set_run()
                else:
                    utl_core.Log.set_module_warning_trace(
                        'look-ass export',
                        u'file="{}" is exists'.format(i_look_ass_file_path)
                    )
                #
                if start_frame is not None and end_frame is not None:
                    i_frame = start_frame, end_frame
                    #
                    mya_fnc_exporters.LookAssExporter(
                        option=dict(
                            file=i_look_ass_file_path,
                            location=root,
                            frame=i_frame,
                            texture_use_environ_map=texture_use_environ_map,
                        )
                    ).set_run()
        else:
            utl_core.Log.set_module_error_trace(
                'ass export',
                'obj="{}" is non-exists'.format(mya_root.path)
            )
