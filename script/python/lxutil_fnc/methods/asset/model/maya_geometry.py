# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        from lxbasic import bsc_core
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        task_properties = self.task_properties
        #
        dcc_pathsep = task_properties.get('dcc.pathsep')
        dcc_root = task_properties.get('dcc.root')
        #
        dcc_root_dag_path = bsc_core.DccPathDagOpt(dcc_root)
        mya_root_dag_path = dcc_root_dag_path.set_translate_to(
            pathsep=dcc_pathsep
        )
        #
        if mya_dcc_objects.Group(mya_root_dag_path.value).get_is_exists() is False:
            self.set_obj_check_result_at(
                mya_root_dag_path.value,
                check_tag='error',
                index=0
            )

    def set_repair_run(self):
        pass

    def set_export_run(self):
        from lxutil import utl_core
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
            pass
        elif scheme == 'publish':
            workspace = 'publish'
            version = rsv_task_properties.get('option.version')
            #
            scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_src_file(
                workspace=workspace,
                version=version
            )
            maya_geometry_export_query = ddl_objects.DdlRsvTaskQuery(
                'maya-geometry-export', rsv_task_properties
            )
            #
            maya_geometry_export = ddl_methods.RsvTaskHookExecutor(
                method_option=maya_geometry_export_query.get_method_option(),
                script_option=maya_geometry_export_query.get_script_option(
                    file=scene_src_file_path,
                    with_geometry_usd=True,
                    with_geometry_uv_map_usd=True,
                    #
                    user=user, time_tag=time_tag
                )
            )
            maya_geometry_export.set_run_with_deadline()
