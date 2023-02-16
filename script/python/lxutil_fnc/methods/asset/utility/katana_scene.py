# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        def yes_fnc_():
            ktn_dcc_objects.Scene.set_file_save()
        #
        from lxutil import utl_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        rsv_task_properties = self.task_properties
        root = rsv_task_properties.get('dcc.root')
        #
        if ktn_dcc_objects.Scene.get_scene_is_dirty():
            w = utl_core.DialogWindow.set_create(
                label='Save',
                content=u'Scene has been modified, Do you want to save change to "{}"'.format(
                    ktn_dcc_objects.Scene.get_current_file_path()
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
        #
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
            rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
            katana_scene_src_file_path = rsv_asset_scene_query.get_katana_src_file(
                version=version
            )
            #
            if bsc_core.ApplicationMtd.get_is_katana():
                import lxkatana.fnc.exporters as ktn_fnc_exporters
                #
                ktn_fnc_exporters.SceneExporter(
                    file_path=katana_scene_src_file_path
                ).set_run()
            else:
                pass
            #
            katana_scene_export_query = ddl_objects.DdlRsvTaskQuery(
                'katana-scene-export', rsv_task_properties
            )
            #
            katana_scene_export = ddl_methods.RsvTaskHookExecutor(
                method_option=katana_scene_export_query.get_method_option(),
                script_option=katana_scene_export_query.get_script_option(
                    file=katana_scene_src_file_path,
                    with_scene=True,
                    with_texture_tx=True,
                    #
                    user=user, time_tag=time_tag,
                    #
                    rez_beta=True,
                ),
            )
            katana_scene_export.execute_with_deadline()
