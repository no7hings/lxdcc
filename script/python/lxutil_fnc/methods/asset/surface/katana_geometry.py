# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        if ktn_dcc_objects.Node('geometries_merge').get_is_exists() is True:
            self._set_old_check_run_()
        else:
            if ktn_dcc_objects.Node('asset_geometries_merge').get_is_exists() is True:
                self._set_new_check_run_()

    def _set_old_check_run_(self):
        import lxbasic.objects as bsc_objects

        from lxutil import utl_configure
        #
        import lxresolver.operators as rsv_operators
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        import lxkatana.fnc.comparers as ktn_fnc_comparers
        #
        from lxresolver import rsv_configure
        #
        task_properties = self.task_properties
        #
        root = task_properties.get('dcc.root')
        #
        location = '/root/world/geo'
        #
        sub_root = '{}/hi'.format(root)
        sub_location = '{}{}/hi'.format(location, root)
        #
        obj = ktn_dcc_objects.Node('set_usd')
        #
        obj_scene = ktn_dcc_objects.Scene()
        obj_scene.load_from_location(
            ktn_obj='geometries_merge',
            root=sub_location,
        )
        obj_universe = obj_scene.universe
        #
        root_obj = obj_universe.get_obj(root)
        sub_root_obj = obj_universe.get_obj(sub_location)
        if sub_root_obj is None:
            self.set_obj_check_result_at(sub_location, check_tag='warning', index=0)
        else:
            rsv_asset_geometry_opt = rsv_operators.RsvAssetGeometryQuery(self.task_properties)
            latest_model_geometry_usd_hi_file_path = rsv_asset_geometry_opt.get_usd_model_hi_file()
            #
            file_paths_1 = []
            if latest_model_geometry_usd_hi_file_path is None:
                file_paths_1 = [latest_model_geometry_usd_hi_file_path]
            #
            if file_paths_1:
                self.set_obj_files_check_result_at(
                    sub_root_obj.path,
                    file_paths=file_paths_1,
                    check_tag='warning',
                    index=1
                )
            #
            work_scene_src_file_path = ktn_dcc_objects.Scene.get_current_file_path()
            #
            fnc_geometry_comparer = ktn_fnc_comparers.FncGeometryComparer(
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
                obj_path = '{}{}'.format(location, i_src_gmt_path)
                for j_e in es:
                    if j_e in i_description:
                        self.set_obj_check_result_at(
                            obj_path,
                            check_tag='error',
                            index=2,
                            description=i_description
                        )
            #
            surface_workspace = ktn_dcc_objects.AssetWorkspace()
            geometry_usd_check_raw = surface_workspace.get_geometry_usd_check_raw()
            if not geometry_usd_check_raw:
                self.set_obj_check_result_at(obj.path, check_tag='error', index=1)
            else:
                set_usd_configure = bsc_objects.Configure(value=rsv_configure.Data.GEOMETRY_USD_CONFIGURE_PATH)
                file_paths_6 = []
                for element_label in set_usd_configure.get_branch_keys('elements'):
                    v = set_usd_configure.get('elements.{}'.format(element_label))
                    keyword = v['keyword']
                    step = v['step']
                    task = v['task']
                    if element_label in geometry_usd_check_raw:
                        current_file_path = geometry_usd_check_raw[element_label]
                        latest_file_path = self._get_latest_geometry_file_path_(keyword, step, task)
                        if latest_file_path != current_file_path:
                            file_paths_6.append(latest_file_path)
                #
                if file_paths_6:
                    self.set_obj_files_check_result_at(obj.path, file_paths=file_paths_6, check_tag='error', index=6)

    def _set_old_repair_run_(self):
        raise RuntimeError(
            'old framework is unused'
        )

    def _set_new_check_run_(self):
        from lxutil import utl_configure
        #
        import lxresolver.operators as rsv_operators
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        import lxkatana.fnc.comparers as ktn_fnc_comparers
        #
        task_properties = self.task_properties
        #
        root = task_properties.get('dcc.root')
        sub_root = '{}/hi'.format(root)
        #
        geometry_location = '/root/world/geo'
        #
        location = '{}{}'.format(geometry_location, root)
        sub_location = '{}{}'.format(geometry_location, sub_root)
        #
        obj_scene = ktn_dcc_objects.Scene()
        obj_scene.load_from_location(
            ktn_obj='asset_geometries_merge',
            root=sub_location,
        )
        obj_universe = obj_scene.universe

        sub_root_obj = obj_universe.get_obj(sub_location)
        if sub_root_obj is None:
            self.set_obj_check_result_at(sub_location, check_tag='warning', index=0)
        else:
            rsv_asset_geometry_opt = rsv_operators.RsvAssetGeometryQuery(self.task_properties)
            latest_model_geometry_usd_hi_file_path = rsv_asset_geometry_opt.get_usd_model_hi_file()
            file_paths_1 = []
            if latest_model_geometry_usd_hi_file_path is None:
                file_paths_1 = [latest_model_geometry_usd_hi_file_path]
            else:
                work_scene_src_file_path = ktn_dcc_objects.Scene.get_current_file_path()
                #
                fnc_geometry_comparer = ktn_fnc_comparers.FncGeometryComparer(
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
                    obj_path = '{}{}'.format(location, i_src_gmt_path)
                    for j_e in es:
                        if j_e in i_description:
                            self.set_obj_check_result_at(
                                obj_path,
                                check_tag='error',
                                index=2,
                                description=i_description
                            )
            #
            if file_paths_1:
                self.set_obj_files_check_result_at(
                    sub_root_obj.path,
                    file_paths=file_paths_1,
                    check_tag='warning',
                    index=1
                )

    def _set_new_repair_run_(self):
        from lxkatana import ktn_core
        if ktn_core.NGObjOpt._get_is_exists_('asset__geometries') is True:
            ktn_core.NGObjOpt('asset__geometries').execute_port(
                'usd.create'
            )

    def _get_latest_geometry_file_path_(self, keyword, step, task):
        import copy
        #
        import lxresolver.commands as rsv_commands
        #
        task_properties = self.task_properties
        resolver = rsv_commands.get_resolver()
        #
        _kwargs = copy.copy(task_properties.value)
        _kwargs['step'] = step
        _kwargs['task'] = task
        #
        rsv_task = resolver.get_rsv_task(**_kwargs)
        #
        geometry_file = rsv_task.get_rsv_unit(
            keyword=keyword,
            workspace='publish',
        )
        geometry_file_path = geometry_file.get_result(version='latest')
        return geometry_file_path

    def set_repair_run(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        if ktn_dcc_objects.Node('geometries_merge').get_is_exists() is True:
            self._set_old_repair_run_()
        else:
            if ktn_dcc_objects.Node('asset_geometries_merge').get_is_exists() is True:
                self._set_new_repair_run_()

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
                katana_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_src_file(
                    version=version
                )
                if step in ['srf']:
                    # main task
                    katana_geometry_export_query = ddl_objects.DdlRsvTaskQuery(
                        'katana-geometry-export', rsv_task_properties
                    )
                    #
                    katana_geometry_exporter = ddl_methods.RsvTaskHookExecutor(
                        method_option=katana_geometry_export_query.get_method_option(),
                        script_option=katana_geometry_export_query.get_script_option(
                            file=katana_scene_src_file_path,
                            with_geometry_usd=True,
                            with_geometry_uv_map_usd=True,
                            #
                            user=user, time_tag=time_tag
                        )
                    )
                    katana_geometry_exporter.execute_with_deadline()
                    #
                    if step in ['srf']:
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
                                                        'katana-geometry-export', rsv_task_properties
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
