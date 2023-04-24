# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        from lxbasic import bsc_core
        #
        from lxutil import utl_configure, utl_core
        #
        import lxresolver.operators as rsv_operators
        #
        from lxmaya import ma_configure
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        import lxmaya.fnc.comparers as mya_fnc_comparers
        #
        rsv_task_properties = self.task_properties
        #
        root = rsv_task_properties.get('dcc.root')
        #
        sub_root = '{}/hi'.format(root)
        #
        sub_root_dag_path = bsc_core.DccPathDagOpt(sub_root)
        sub_root_mya_dag_path = sub_root_dag_path.translate_to(ma_configure.Util.OBJ_PATHSEP)
        #
        sub_root_mya_obj = mya_dcc_objects.Group(sub_root_mya_dag_path.path)
        if sub_root_mya_obj.get_is_exists() is False:
            self.set_obj_check_result_at(
                sub_root_mya_obj.path,
                check_tag='warning',
                index=0
            )
        else:
            rsv_asset_geometry_opt = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
            latest_model_geometry_usd_hi_file_path = rsv_asset_geometry_opt.get_usd_model_hi_file()
            #
            file_paths_1 = []
            if latest_model_geometry_usd_hi_file_path is None:
                file_paths_1 = [latest_model_geometry_usd_hi_file_path]
            #
            if file_paths_1:
                self.set_obj_files_check_result_at(
                    sub_root_mya_obj.path,
                    file_paths=file_paths_1,
                    check_tag='warning',
                    index=1
                )
            #
            work_scene_src_file_path = mya_dcc_objects.Scene.get_current_file_path()
            fnc_geometry_comparer = mya_fnc_comparers.FncGeometryComparer(
                work_scene_src_file_path, sub_root
            )
            es = [
                utl_configure.DccMeshCheckStatus.ADDITION,
                utl_configure.DccMeshCheckStatus.DELETION,
                utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
                utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
            ]
            results = fnc_geometry_comparer.get_results()
            for i_src_gmt_path, i_tgt_gmt_path, i_description in results:
                i_src_gmt_path_dag_opt = bsc_core.DccPathDagOpt(i_src_gmt_path)
                i_mya_path_dag_opt = i_src_gmt_path_dag_opt.translate_to(ma_configure.Util.OBJ_PATHSEP)
                for j_e in es:
                    if j_e in i_description:
                        self.set_obj_check_result_at(
                            i_mya_path_dag_opt.get_value(),
                            check_tag='error',
                            index=2,
                            description=i_description
                        )
            #
            geometry_paths = sub_root_mya_obj.get_all_shape_paths(include_obj_type=['mesh'])
            if geometry_paths:
                gp = utl_core.GuiProgressesRunner(maximum=len(geometry_paths), label='geometry-check-run')
                for seq, i_geometry_path in enumerate(geometry_paths):
                    gp.set_update()
                    mesh_obj = mya_dcc_objects.Mesh(i_geometry_path)
                    mesh_obj_opt = mya_dcc_operators.MeshOpt(mesh_obj)
                    if mesh_obj_opt.get_default_uv_map_is_exists() is False:
                        self.set_obj_check_result_at(
                            mesh_obj.path,
                            check_tag='error',
                            index=3
                        )
                    else:
                        uv_map_check_error_result = mesh_obj_opt.get_uv_map_check_error_result()
                        if uv_map_check_error_result:
                            self.set_obj_comps_check_result_at(
                                mesh_obj.path,
                                comp_names=uv_map_check_error_result,
                                check_tag='error',
                                index=4
                            )
                    #
                    look_obj_opt = mya_dcc_operators.MeshLookOpt(mesh_obj)
                    face_assign_comp_names = look_obj_opt.get_face_assign_comp_names()
                    if face_assign_comp_names:
                        self.set_obj_comps_check_result_at(
                            mesh_obj.path,
                            comp_names=face_assign_comp_names,
                            check_tag='error',
                            index=5
                        )
                gp.set_stop()

    def set_repair_run(self):
        from lxbasic import bsc_core

        from lxutil import utl_core
        #
        from lxmaya import ma_configure
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        rsv_task_properties = self.task_properties
        #
        root = rsv_task_properties.get('dcc.root')
        #
        sub_root = '{}/hi'.format(root)
        #
        sub_root_dag_path = bsc_core.DccPathDagOpt(sub_root)
        sub_root_mya_dag_path = sub_root_dag_path.translate_to(ma_configure.Util.OBJ_PATHSEP)
        #
        sub_root_mya_obj = mya_dcc_objects.Group(sub_root_mya_dag_path.path)
        if sub_root_mya_obj.get_is_exists() is True:
            geometry_paths = sub_root_mya_obj.get_all_shape_paths(include_obj_type=['mesh'])
            if geometry_paths:
                ps = utl_core.Progress.set_create(maximum=len(geometry_paths))
                for seq, geometry_path in enumerate(geometry_paths):
                    utl_core.Progress.set_update(ps)
                    mesh_obj = mya_dcc_objects.Mesh(geometry_path)
                    mesh_obj_opt = mya_dcc_operators.MeshOpt(mesh_obj)
                    if mesh_obj_opt.get_default_uv_map_is_exists() is False:
                        mesh_obj_opt.set_uv_map_repair()
                utl_core.Progress.set_stop(ps)

    def set_export_run(self):
        import copy
        #
        from lxutil import utl_core
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxresolver.commands as rsv_commands
        #
        import lxresolver.operators as rsv_operators
        #
        rsv_task_properties = self.task_properties
        #
        user = rsv_task_properties.get('user') or utl_core.System.get_user_name()
        time_tag = rsv_task_properties.get('time_tag') or utl_core.System.get_time_tag()
        #
        branch = rsv_task_properties.get('branch')
        step = rsv_task_properties.get('step')
        task = rsv_task_properties.get('task')
        #
        if branch == 'asset':
            scheme = rsv_task_properties.get('option.scheme')
            if scheme == 'work':
                version = rsv_task_properties.get('version')
            elif scheme == 'publish':
                version = rsv_task_properties.get('option.version')
                #
                maya_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_src_file(
                    version=version
                )
                # surface
                if step in ['srf']:
                    # main task
                    maya_geometry_export_query = ddl_objects.DdlRsvTaskQuery(
                        'maya-geometry-export', rsv_task_properties
                    )
                    maya_geometry_export = ddl_methods.RsvTaskHookExecutor(
                        method_option=maya_geometry_export_query.get_method_option(),
                        script_option=maya_geometry_export_query.get_script_option(
                            file=maya_scene_src_file_path,
                            with_geometry_usd=True,
                            with_geometry_uv_map_usd=True,
                            #
                            user=user, time_tag=time_tag,
                        )
                    )
                    maya_geometry_export.execute_with_deadline()
                    # import geometry uv-map
                    if task in ['surfacing']:
                        resolver = rsv_commands.get_resolver()
                        for i_step, i_task in [
                            ('mod', 'modeling'),
                            # ('rig', 'rigging'),
                        ]:
                            i_kwargs = copy.copy(rsv_task_properties.value)
                            i_kwargs['step'] = i_step
                            i_kwargs['task'] = i_task
                            i_rsv_task = resolver.get_rsv_task(**i_kwargs)
                            if i_rsv_task is not None:
                                i_maya_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-maya-scene-file')
                                i_maya_scene_src_file_path = i_maya_scene_src_file_unit.get_result(version='latest')
                                if i_maya_scene_src_file_path is not None:
                                    i_maya_geometry_import_query = ddl_objects.DdlRsvTaskQuery(
                                        'maya-geometry-import', rsv_task_properties
                                    )
                                    #
                                    i_maya_geometry_import = ddl_methods.RsvTaskHookExecutor(
                                        method_option=i_maya_geometry_import_query.get_method_option(),
                                        script_option=i_maya_geometry_import_query.get_script_option(
                                            file=i_maya_scene_src_file_path,
                                            with_scene=True,
                                            with_geometry_uv_map=True,
                                            #
                                            user=user, time_tag=time_tag,
                                        ),
                                        job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                                            [
                                                ddl_objects.DdlRsvTaskQuery(
                                                    'maya-geometry-export', rsv_task_properties
                                                ).get_method_option(),
                                            ]
                                        )
                                    )
                                    #
                                    i_maya_geometry_import.execute_with_deadline()
                            else:
                                utl_core.Log.set_module_warning_trace(
                                    'maya-geometry-uv-map-import',
                                    'task="{}/{}" is non-exists'.format(i_step, i_task)
                                )
