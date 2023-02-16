# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        def yes_fnc_():
            maya_dcc_objects.Scene.set_file_save()
        #
        from lxutil import utl_core
        #
        import lxmaya.dcc.dcc_objects as maya_dcc_objects
        #
        rsv_task_properties = self.task_properties
        root = rsv_task_properties.get('dcc.root')
        #
        if maya_dcc_objects.Scene.get_scene_is_dirty():
            w = utl_core.DialogWindow.set_create(
                label='Save',
                content=u'Scene has been modified, Do you want to save change to "{}"'.format(
                    maya_dcc_objects.Scene.get_current_file_path()
                ),
                window_size=(480, 160),
                #
                yes_method=yes_fnc_,
                #
                yes_label='Save',
                no_label='Don\'t save'
            )

            result = w.get_result()
            if result is True:
                pass
            else:
                self.set_obj_check_result_at(
                    root,
                    check_tag='error',
                    index=0
                )

    def set_export_run(self):
        from lxbasic import bsc_core

        from lxutil import utl_core
        #
        import lxresolver.operators as rsv_operators
        #
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        rsv_task_properties = self.task_properties
        #
        user = rsv_task_properties.get('user') or utl_core.System.get_user_name()
        time_tag = rsv_task_properties.get('time_tag') or utl_core.System.get_time_tag()
        #
        task = rsv_task_properties.get('task')
        #
        scheme = rsv_task_properties.get('option.scheme')
        if scheme == 'work':
            version = rsv_task_properties.get('version')
        elif scheme == 'publish':
            version = rsv_task_properties.get('option.version')
            #
            maya_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
                version=version
            )
            #
            if bsc_core.ApplicationMtd.get_is_maya():
                import lxmaya.fnc.exporters as mya_fnc_exporters
                #
                mya_fnc_exporters.SceneExporter(
                    option=dict(
                        file=maya_scene_src_file_path,
                        with_xgen_collection=True
                    )
                ).set_run()
            else:
                pass
            #
            maya_scene_export_query = ddl_objects.DdlRsvTaskQuery(
                'maya-scene-export', rsv_task_properties
            )
            if task in ['srf_anishading']:
                maya_scene_export_script_option = maya_scene_export_query.get_script_option(
                    file=maya_scene_src_file_path,
                    with_scene=True,
                    with_snapshot_preview=True,
                    with_texture=True,
                    #
                    user=user, time_tag=time_tag,
                    #
                    rez_beta=True,
                )
            else:
                maya_scene_export_script_option = maya_scene_export_query.get_script_option(
                    file=maya_scene_src_file_path,
                    with_scene=True,
                    with_snapshot_preview=True,
                    with_texture_tx=True,
                    #
                    user=user, time_tag=time_tag,
                    #
                    rez_beta=True,
                )
            #
            maya_scene_export = ddl_methods.RsvTaskHookExecutor(
                method_option=maya_scene_export_query.get_method_option(),
                script_option=maya_scene_export_script_option
            )
            maya_scene_export.execute_with_deadline()
