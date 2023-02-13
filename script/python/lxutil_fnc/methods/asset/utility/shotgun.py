# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        import lxshotgun.objects as stg_objects
        #
        import lxshotgun.operators as stg_operators
        #
        task_properties = self.task_properties
        root = task_properties.get('dcc.root')
        #
        stg_connector = stg_objects.StgConnector()
        sgt_task_query = stg_connector.get_stg_task_query(**task_properties.value)
        if sgt_task_query is not None:
            stg_task_opt = stg_operators.StgTaskOpt(sgt_task_query)
            status = stg_task_opt.get_stg_status()
            if status in ['omt', 'hld']:
                self.set_obj_check_result_at(root, check_tag='warning', index=1)
        else:
            self.set_obj_check_result_at(root, check_tag='warning', index=0)

    def set_repair_run(self):
        pass

    def set_export_run(self):
        from lxutil import utl_core
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxresolver.operators as rsv_operators
        #
        rsv_task_properties = self.task_properties
        #
        user = rsv_task_properties.get('user') or utl_core.System.get_user_name()
        time_tag = rsv_task_properties.get('time_tag') or utl_core.System.get_time_tag()
        #
        scheme = rsv_task_properties.get('option.scheme')
        if scheme == 'work':
            version = rsv_task_properties.get('version')
        elif scheme == 'publish':
            workspace = 'publish'
            version = rsv_task_properties.get('option.version')
            #
            dcc_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_src_file(
                workspace=workspace,
                version=version
            )
            # shotgun
            shotgun_export_query = ddl_objects.DdlRsvTaskQuery(
                'shotgun-export', rsv_task_properties
            )
            shotgun_export = ddl_methods.RsvTaskHookExecutor(
                method_option=shotgun_export_query.get_method_option(),
                script_option=shotgun_export_query.get_script_option(
                    file=dcc_scene_src_file_path,
                    with_shotgun_version=True,
                    with_link=True,
                    with_shotgun_dependency=True,
                    #
                    user=user, time_tag=time_tag
                ),
                job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                    [
                        # maya-scene-export
                        ddl_objects.DdlRsvTaskQuery('maya-scene-export', rsv_task_properties).get_method_option(),
                        # katana-scene-export
                        ddl_objects.DdlRsvTaskQuery('katana-scene-export', rsv_task_properties).get_method_option(),
                        # maya-geometry-export
                        ddl_objects.DdlRsvTaskQuery('maya-geometry-export', rsv_task_properties).get_method_option(),
                        # katana-geometry-export
                        ddl_objects.DdlRsvTaskQuery('katana-geometry-export', rsv_task_properties).get_method_option(),
                        # maya-look-export
                        ddl_objects.DdlRsvTaskQuery('maya-look-export', rsv_task_properties).get_method_option(),
                        # katana-look-export
                        ddl_objects.DdlRsvTaskQuery('katana-look-export', rsv_task_properties).get_method_option(),
                        # usd-export
                        ddl_objects.DdlRsvTaskQuery('usd-export', rsv_task_properties).get_method_option(),
                    ]
                )
            )
            shotgun_export.set_run_with_deadline()
