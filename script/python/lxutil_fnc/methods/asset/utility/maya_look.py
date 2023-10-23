# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        from lxmaya import ma_configure
        #
        task = self.task_properties.get('task')
        root = self.task_properties.get('dcc.root')
        #
        sub_root = '{}/hi'.format(root)
        #
        sub_root_dag_path = bsc_core.DccPathDagOpt(sub_root)
        sub_root_mya_dag_path = sub_root_dag_path.translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        #
        sub_root_mya_obj = mya_dcc_objects.Node(sub_root_mya_dag_path.path)
        #
        if sub_root_mya_obj.get_is_exists() is True:
            objs = sub_root_mya_obj.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(objs)
            includes = objs_look_opt.get_texture_reference_paths()
            #
            if includes:
                objs = mya_dcc_objects.TextureReferences._get_objs_(includes)
                if objs:
                    gp = bsc_core.LogProcessContext(maximum=len(objs), label='texture-check-run')
                    name_base_dict = {}
                    texture_name_match_obj_dic = {}
                    texture_name_match_texture_path_dic = {}
                    #
                    for i_obj in objs:
                        gp.set_update()
                        #
                        file_paths_0 = []
                        file_paths_1 = []
                        file_paths_2 = []
                        file_paths_3 = []
                        file_paths_4 = []
                        #
                        file_paths_6 = []
                        file_paths_7 = []
                        for j_port_path, j_file_path in i_obj.reference_raw.items():
                            stg_texture = utl_dcc_objects.OsTexture(j_file_path)
                            exists_files = stg_texture.get_exists_files_()
                            #
                            if not exists_files:
                                file_paths_0.append(stg_texture.path)
                            else:
                                if task in ['srf_anishading']:
                                    if stg_texture.get_ext_is('.jpg') is False:
                                        file_paths_6.append(stg_texture.path)
                                    #
                                    if stg_texture.get_is_exists_as_tgt_ext('.jpg') is False:
                                        file_paths_7.append(stg_texture.path)
                                else:
                                    if stg_texture.get_ext_is('.tx') is False:
                                        file_paths_1.append(stg_texture.path)
                                    #
                                    if stg_texture.get_is_exists_as_tgt_ext('.tx') is False:
                                        file_paths_2.append(stg_texture.path)
                                #
                                if bsc_core.RawTextOpt(j_file_path).get_is_contain_chinese() is True:
                                    file_paths_3.append(stg_texture.path)
                                #
                                if bsc_core.RawTextOpt(j_file_path).get_is_contain_space() is True:
                                    file_paths_4.append(stg_texture.path)
                                #
                                name_base = stg_texture.name_base
                                #
                                texture_name_match_obj_dic.setdefault(
                                    name_base, []
                                ).append(i_obj)
                                texture_name_match_texture_path_dic.setdefault(
                                    name_base, []
                                ).append(j_file_path)
                        #
                        if file_paths_0:
                            self.set_obj_files_check_result_at(
                                i_obj.path, file_paths=file_paths_0, check_tag='error', index=0
                            )
                        if file_paths_1:
                            self.set_obj_files_check_result_at(
                                i_obj.path, file_paths=file_paths_1, check_tag='error', index=1
                            )
                        if file_paths_2:
                            self.set_obj_files_check_result_at(
                                i_obj.path, file_paths=file_paths_2, check_tag='error', index=2
                            )
                        if file_paths_3:
                            self.set_obj_files_check_result_at(
                                i_obj.path, file_paths=file_paths_3, check_tag='warning', index=3
                            )
                        if file_paths_4:
                            self.set_obj_files_check_result_at(
                                i_obj.path, file_paths=file_paths_4, check_tag='warning', index=4
                            )
                        if file_paths_6:
                            self.set_obj_files_check_result_at(
                                i_obj.path, file_paths=file_paths_6, check_tag='error', index=6
                            )

                    for k, v in texture_name_match_texture_path_dic.items():
                        if len(list(set(v))) > 1:
                            if k in texture_name_match_obj_dic:
                                error_objs = texture_name_match_obj_dic[k]
                                for i_error_obj in error_objs:
                                    self.set_obj_files_check_result_at(
                                        i_error_obj.path, file_paths=v, check_tag='error', index=5
                                    )
                    #
                    gp.set_stop()
        else:
            bsc_core.Log.trace_method_warning(
                'look-method-check-run',
                u'obj="{}" is non-exists'.format(sub_root)
            )

    def set_repair_run(self):
        from lxbasic import bsc_core

        import lxutil.dcc.dcc_operators as utl_dcc_operators
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        from lxutil import utl_core
        #
        from lxmaya import ma_configure
        #
        task = self.task_properties.get('task')
        root = self.task_properties.get('dcc.root')
        sub_root = '{}/hi'.format(root)
        #
        sub_root_dag_path = bsc_core.DccPathDagOpt(sub_root)
        sub_root_mya_dag_path = sub_root_dag_path.translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        #
        sub_root_mya_obj = mya_dcc_objects.Group(sub_root_mya_dag_path.path)
        if sub_root_mya_obj.get_is_exists() is True:
            objs = sub_root_mya_obj.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(objs)
            includes = objs_look_opt.get_texture_reference_paths()
            if includes:
                objs = mya_dcc_objects.TextureReferences._get_objs_(includes)
                if task in ['srf_anishading']:
                    utl_dcc_operators.DccTexturesOpt(
                        mya_dcc_objects.TextureReferences(
                            option=dict(with_reference=False)
                        ),
                        includes=objs
                    ).set_jpg_create_and_repath()
                else:
                    utl_dcc_operators.DccTexturesOpt(
                        mya_dcc_objects.TextureReferences(
                            option=dict(with_reference=False)
                        ),
                        includes=objs
                    ).set_tx_create_and_repath()
        else:
            bsc_core.Log.trace_method_warning(
                'look-method-check-run',
                'obj="{}" is non-exists'.format(sub_root)
            )

    def set_export_run(self):
        from lxutil import utl_core
        #
        rsv_task_properties = self.task_properties
        #
        user = rsv_task_properties.get('user') or utl_core.System.get_user_name()
        time_tag = rsv_task_properties.get('time_tag') or utl_core.System.get_time_tag()
        #
        branch = rsv_task_properties.get('branch')
        step = rsv_task_properties.get('step')
        if branch == 'asset' and step in ['mod', 'srf']:
            scheme = rsv_task_properties.get('option.scheme')
            if scheme == 'work':
                version = rsv_task_properties.get('version')
            elif scheme == 'publish':
                self.__set_maya_look_export_(user, time_tag)
                #
                self.__set_maya_proxy_export_(user, time_tag)
                #
                self.__set_katana_look_export_(user, time_tag)
                self.__set_katana_cfx_look_export(user, time_tag)
                # self.__set_katana_render_export_(user, time_tag)
                #
                self.__set_maya_look_preview_export_(user, time_tag)
                #
                self.__set_maya_look_import_(user, time_tag)

    def __set_maya_look_export_(self, user, time_tag):
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxresolver.operators as rsv_operators
        #
        rsv_task_properties = self.task_properties
        #
        task = rsv_task_properties.get('task')
        version = rsv_task_properties.get('option.version')
        #
        maya_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
            version=version
        )
        # maya look export
        maya_look_export_query = ddl_objects.DdlRsvTaskQuery(
            'maya-look-export', rsv_task_properties
        )
        if task in ['srf_anishading']:
            maya_scene_export_script_option = maya_look_export_query.get_script_option(
                file=maya_scene_src_file_path,
                with_look_ass=True,
                with_look_properties_usd=False,
                with_look_yml=True,
                with_texture=True,
                #
                user=user, time_tag=time_tag,
                #
                rez_beta=True,
            )
        else:
            maya_scene_export_script_option = maya_look_export_query.get_script_option(
                file=maya_scene_src_file_path,
                with_look_ass=True,
                with_look_properties_usd=False,
                with_look_yml=True,
                with_texture_tx=True,
                #
                user=user, time_tag=time_tag,
                #
                rez_beta=True,
            )
        #
        maya_look_export = ddl_methods.RsvTaskHookExecutor(
            method_option=maya_look_export_query.get_method_option(),
            script_option=maya_scene_export_script_option
        )
        maya_look_export.execute_with_deadline()

    def __set_maya_look_preview_export_(self, user, time_tag):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxresolver.commands as rsv_commands
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        resolver = rsv_commands.get_resolver()
        #
        rsv_task_properties = self.task_properties
        task = rsv_task_properties.get('task')
        if task in ['surfacing']:
            if rsv_task_properties:
                project = rsv_task_properties.get('project')
                asset = rsv_task_properties.get('asset')
                #
                look_preview_task = resolver.get_rsv_task(
                    project=project, asset=asset, step='srf', task='srf_anishading'
                )
                if look_preview_task is not None:
                    scene_src_maya_file_unit = look_preview_task.get_rsv_unit(
                        keyword='asset-maya-scene-src-file'
                    )
                    scene_src_maya_file_path = scene_src_maya_file_unit.get_result(
                        version='new'
                    )
                    #
                    utl_dcc_objects.OsFile(scene_src_maya_file_path).create_directory()
                    #
                    maya_look_preview_export_query = ddl_objects.DdlRsvTaskQuery(
                        'maya-look-preview-export', rsv_task_properties
                    )
                    #
                    maya_look_preview_export = ddl_methods.RsvTaskHookExecutor(
                        method_option=maya_look_preview_export_query.get_method_option(),
                        script_option=maya_look_preview_export_query.get_script_option(
                            file=scene_src_maya_file_path,
                            #
                            create_scene_src=True,
                            with_scene=True,
                            with_work_scene_src=True,
                            #
                            user=user, time_tag=time_tag,
                            #
                            rez_beta=True,
                        ),
                        job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                            [
                                # usd-export
                                ddl_objects.DdlRsvTaskQuery(
                                    'usd-export', rsv_task_properties
                                ).get_method_option(),
                            ]
                        )
                    )
                    maya_look_preview_export.execute_with_deadline()

    def __set_maya_proxy_export_(self, user, time_tag):
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
        version = rsv_task_properties.get('option.version')
        #
        maya_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
            version=version
        )
        # maya proxy export
        maya_proxy_export_query = ddl_objects.DdlRsvTaskQuery(
            'maya-proxy-export', rsv_task_properties
        )
        #
        maya_proxy_export = ddl_methods.RsvTaskHookExecutor(
            method_option=maya_proxy_export_query.get_method_option(),
            script_option=maya_proxy_export_query.get_script_option(
                file=maya_scene_src_file_path,
                with_proxy_xarc=True,
                #
                user=user, time_tag=time_tag,
                #
                rez_beta=True,
            ),
            job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                [
                    # maya-look-export
                    ddl_objects.DdlRsvTaskQuery(
                        'maya-look-export', rsv_task_properties
                    ).get_method_option(),
                ]
            )
        )
        maya_proxy_export.execute_with_deadline()

    def __set_katana_look_export_(self, user, time_tag):
        import lxdeadline.objects as ddl_objects
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxresolver.operators as rsv_operators
        #
        rsv_task_properties = self.task_properties
        #
        version = rsv_task_properties.get('option.version')
        # katana scene export
        katana_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_katana_src_file(
            version=version
        )
        katana_scene_export_query = ddl_objects.DdlRsvTaskQuery(
            'katana-scene-export', rsv_task_properties
        )
        #
        katana_scene_export = ddl_methods.RsvTaskHookExecutor(
            method_option=katana_scene_export_query.get_method_option(),
            script_option=katana_scene_export_query.get_script_option(
                file=katana_scene_src_file_path,
                create_scene_src=True,
                with_scene=True,
                with_texture_tx=True,
                #
                user=user, time_tag=time_tag,
                #
                rez_beta=True,
            ),
            job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                [
                    # maya-geometry-export
                    ddl_objects.DdlRsvTaskQuery(
                        'maya-geometry-export', rsv_task_properties
                    ).get_method_option(),
                    # maya-look-export
                    ddl_objects.DdlRsvTaskQuery(
                        'maya-look-export', rsv_task_properties
                    ).get_method_option(),
                ]
            )
        )
        katana_scene_export.execute_with_deadline()
        # katana look export
        katana_look_export_query = ddl_objects.DdlRsvTaskQuery(
            'katana-look-export', rsv_task_properties
        )
        #
        katana_look_export = ddl_methods.RsvTaskHookExecutor(
            method_option=katana_look_export_query.get_method_option(),
            script_option=katana_look_export_query.get_script_option(
                file=katana_scene_src_file_path,
                with_look_ass=False,
                with_look_klf=True,
                with_texture_tx=True,
                #
                user=user, time_tag=time_tag,
                #
                rez_beta=True,
            ),
            job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                [
                    # katana-scene-export
                    katana_scene_export.get_method_option(),
                ]
            )
        )
        katana_look_export.execute_with_deadline()

    def __set_katana_cfx_look_export(self, user, time_tag):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
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
        task = rsv_task_properties.get('task')
        version = rsv_task_properties.get('option.version')
        # katana cfx look export
        if task in ['srf_anishading']:
            surface_cfx_katana_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(
                rsv_task_properties
            ).get_surface_cfx_katana_src_file(
                version=version
            )
            utl_dcc_objects.OsFile(surface_cfx_katana_scene_src_file_path).create_directory()
            katana_cfx_look_export_query = ddl_objects.DdlRsvTaskQuery(
                'katana-cfx-look-export', rsv_task_properties
            )
            #
            katana_cfx_look_export = ddl_methods.RsvTaskHookExecutor(
                method_option=katana_cfx_look_export_query.get_method_option(),
                script_option=katana_cfx_look_export_query.get_script_option(
                    file=surface_cfx_katana_scene_src_file_path,
                    create_scene_src=True,
                    with_scene=True,
                    with_texture=True,
                    #
                    user=user, time_tag=time_tag,
                    #
                    rez_beta=True,
                ),
                job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                    [
                        # maya-geometry-export
                        ddl_objects.DdlRsvTaskQuery(
                            'maya-geometry-export', rsv_task_properties
                        ).get_method_option(),
                        # maya-look-export
                        ddl_objects.DdlRsvTaskQuery(
                            'maya-look-export', rsv_task_properties
                        ).get_method_option(),
                    ]
                )
            )
            katana_cfx_look_export.execute_with_deadline()
            #
            surface_cfx_maya_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(
                rsv_task_properties).get_surface_cfx_maya_src_file(
                version=version
            )
            utl_dcc_objects.OsFile(surface_cfx_maya_scene_src_file_path).create_directory()
            maya_cfx_look_export_query = ddl_objects.DdlRsvTaskQuery(
                'maya-cfx-look-export', rsv_task_properties
            )
            #
            maya_cfx_look_export = ddl_methods.RsvTaskHookExecutor(
                method_option=maya_cfx_look_export_query.get_method_option(),
                script_option=maya_cfx_look_export_query.get_script_option(
                    file=surface_cfx_maya_scene_src_file_path,
                    create_scene_src=True,
                    with_scene=True,
                    with_texture=True,
                    with_look=True,
                    with_usd_set=True,
                    #
                    user=user, time_tag=time_tag,
                    #
                    rez_beta=True,
                ),
                job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                    [
                        # katana-cfx-look-export
                        katana_cfx_look_export_query.get_method_option()
                    ]
                )
            )
            maya_cfx_look_export.execute_with_deadline()

    def __set_katana_render_export_(self, user, time_tag):
        import lxdeadline.objects as ddl_objects
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxresolver.operators as rsv_operators
        #
        rsv_task_properties = self.task_properties
        #
        task = rsv_task_properties.get('task')
        if task in ['surfacing']:
            version = rsv_task_properties.get('option.version')
            # katana scene export
            katana_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_katana_src_file(
                version=version
            )
            katana_render_export_query = ddl_objects.DdlRsvTaskQuery(
                'katana-render-export', rsv_task_properties
            )
            katana_render_export = ddl_methods.RsvTaskHookExecutor(
                method_option=katana_render_export_query.get_method_option(),
                script_option=katana_render_export_query.get_script_option(
                    file=katana_scene_src_file_path,
                    create_camera=True,
                    create_scene=True,
                    create_render=True,
                    #
                    with_shotgun_render=True,
                    width=1024, height=1024,
                    #
                    user=user, time_tag=time_tag,
                    #
                    rez_beta=True,
                ),
                job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                    [
                        # katana-look-export
                        ddl_objects.DdlRsvTaskQuery(
                            'katana-look-export', rsv_task_properties
                        ).get_method_option(),
                    ]
                )
            )
            katana_render_export.execute_with_deadline()

    def __set_maya_look_import_(self, user, time_tag):
        import copy

        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        from lxdeadline import ddl_core
        #
        import lxresolver.commands as rsv_commands

        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        rsv_task_properties = self.task_properties
        #
        task = rsv_task_properties.get('task')
        # maya look import
        if task in ['srf_anishading']:
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
                        i_maya_look_import_query = ddl_objects.DdlRsvTaskQuery(
                            'maya-look-import', rsv_task_properties
                        )
                        #
                        i_maya_look_import = ddl_methods.RsvTaskHookExecutor(
                            method_option=i_maya_look_import_query.get_method_option(),
                            script_option=i_maya_look_import_query.get_script_option(
                                file=i_maya_scene_src_file_path,
                                with_scene=True,
                                with_surface_preview=True,
                                #
                                user=user, time_tag=time_tag,
                                #
                                rez_beta=True,
                            ),
                            job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                                [
                                    # maya-look-export
                                    ddl_objects.DdlRsvTaskQuery(
                                        'maya-look-export', rsv_task_properties
                                    ).get_method_option(),
                                ]
                            )
                        )
                        #
                        i_maya_look_import.execute_with_deadline()
                else:
                    bsc_core.Log.trace_method_warning(
                        'maya-geometry-uv-map-import',
                        'task="{}/{}" is non-exists'.format(i_step, i_task)
                    )
