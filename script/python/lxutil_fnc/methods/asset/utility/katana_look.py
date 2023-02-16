# coding:utf-8
from lxutil_fnc.objects import utl_fnc_obj_abs


class Method(utl_fnc_obj_abs.AbsTaskMethod):
    def __init__(self, properties):
        super(Method, self).__init__(properties)

    def set_check_run(self):
        from lxbasic import bsc_core
        #
        import lxbasic.objects as bsc_objects
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        from lxutil import utl_core
        #
        exclude_paths = [i.path for i in ktn_dcc_objects.AndShaders.get_objs() if i.path.startswith('/rootNode/light_rigs')]
        objs = ktn_dcc_objects.TextureReferences().get_objs(exclude_paths=exclude_paths)
        if objs:
            check_dict = {}
            texture_name_match_obj_dic = {}
            texture_name_match_texture_path_dic = {}
            ps = utl_core.Progress.set_create(len(objs))
            for i_obj in objs:
                utl_core.Progress.set_update(ps)
                #
                file_paths_0 = []
                file_paths_1 = []
                file_paths_2 = []
                file_paths_3 = []
                file_paths_4 = []
                i_check_results = [
                    file_paths_0, file_paths_1, file_paths_2, file_paths_3, file_paths_4
                ]
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    stg_texture = utl_dcc_objects.OsTexture(j_file_path)
                    texture_tile_file_objs = stg_texture.get_exists_files_()
                    if j_file_path in check_dict:
                        j_check_results = check_dict[j_file_path]
                    else:
                        j_check_results = [True]*5
                        check_dict[j_file_path] = j_check_results
                        if not texture_tile_file_objs:
                            j_check_results[0] = False
                        else:
                            if stg_texture.get_ext_is_tx() is False:
                                j_check_results[1] = False
                            #
                            if stg_texture.get_is_exists_as_tx() is False:
                                j_check_results[2] = False
                            #
                            if bsc_core.RawTextOpt(j_file_path).get_is_contain_chinese() is True:
                                j_check_results[3] = False
                            #
                            if bsc_core.RawTextOpt(j_file_path).get_is_contain_space() is True:
                                j_check_results[4] = False
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
                    for index, k_check_result in enumerate(j_check_results):
                        if k_check_result is False:
                            i_check_results[index].append(j_file_path)
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
            #
            for k, v in texture_name_match_texture_path_dic.items():
                if len(list(set(v))) > 1:
                    if k in texture_name_match_obj_dic:
                        error_objs = texture_name_match_obj_dic[k]
                        for i_error_obj in error_objs:
                            self.set_obj_files_check_result_at(
                                i_error_obj.path, file_paths=v, check_tag='error', index=5
                            )
            #
            utl_core.Progress.set_stop(ps)

    def set_repair_run(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        import lxutil.dcc.dcc_operators as utl_dcc_operators
        #
        utl_dcc_operators.DccTexturesOpt(
            ktn_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_tx_create_and_repath()

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
                self.__set_katana_look_export_(user, time_tag)
                # self.__set_katana_render_export_(user, time_tag)
                #
                self.__set_maya_scene_export_(user, time_tag)
                #
                self.__set_maya_look_export_(user, time_tag)
                #
                self.__set_maya_proxy_export_(user, time_tag)
                #
                self.__set_maya_look_preview_export_(user, time_tag)

    def __set_katana_look_export_(self, user, time_tag):
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
        rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
        katana_scene_src_file_path = rsv_asset_scene_query.get_katana_src_file(
            version=version
        )
        katana_look_export_query = ddl_objects.DdlRsvTaskQuery(
            'katana-look-export', rsv_task_properties
        )
        #
        katana_look_export = ddl_methods.RsvTaskHookExecutor(
            method_option=katana_look_export_query.get_method_option(),
            script_option=katana_look_export_query.get_script_option(
                file=katana_scene_src_file_path,
                with_look_ass=True,
                with_look_properties_usd=False,
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
                    ddl_objects.DdlRsvTaskQuery(
                        'katana-scene-export', rsv_task_properties
                    ).get_method_option(),
                ]
            )
        )
        katana_look_export.execute_with_deadline()

    def __set_katana_render_export_(self, user, time_tag):
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
        if task in ['surfacing']:
            version = rsv_task_properties.get('option.version')
            #
            rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
            katana_scene_src_file_path = rsv_asset_scene_query.get_katana_src_file(
                version=version
            )
            #
            katana_render_export_query = ddl_objects.DdlRsvTaskQuery(
                'katana-render-export', rsv_task_properties
            )
            #
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

    def __set_maya_scene_export_(self, user, time_tag):
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
        rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
        #
        maya_scene_src_file_path = rsv_asset_scene_query.get_maya_src_file(
            version=version
        )
        maya_scene_export_query = ddl_objects.DdlRsvTaskQuery(
            'maya-scene-export', rsv_task_properties
        )
        # maya-scene
        maya_scene_export = ddl_methods.RsvTaskHookExecutor(
            method_option=maya_scene_export_query.get_method_option(),
            script_option=maya_scene_export_query.get_script_option(
                file=maya_scene_src_file_path,
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
                    # katana-geometry
                    ddl_objects.DdlRsvTaskQuery(
                        'katana-geometry-export', rsv_task_properties
                    ).get_method_option(),
                    # katana-look
                    ddl_objects.DdlRsvTaskQuery(
                        'katana-look-export', rsv_task_properties
                    ).get_method_option(),
                ]
            )
        )
        maya_scene_export.execute_with_deadline()

    def __set_maya_look_export_(self, user, time_tag):
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
        rsv_asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
        #
        maya_scene_src_file_path = rsv_asset_scene_query.get_maya_src_file(
            version=version
        )
        #
        maya_look_export_query = ddl_objects.DdlRsvTaskQuery(
            'maya-look-export', rsv_task_properties
        )
        #
        maya_look_export = ddl_methods.RsvTaskHookExecutor(
            method_option=maya_look_export_query.get_method_option(),
            script_option=maya_look_export_query.get_script_option(
                file=maya_scene_src_file_path,
                with_look_ass=True,
                with_texture_tx=True,
                #
                user=user, time_tag=time_tag,
                #
                rez_beta=True,
            ),
            job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
                [
                    # maya-scene
                    ddl_objects.DdlRsvTaskQuery(
                        'maya-scene-export', rsv_task_properties
                    ).get_method_option(),
                ]
            )
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
                    utl_dcc_objects.OsFile(scene_src_maya_file_path).set_directory_create()
                    #
                    maya_look_export_query = ddl_objects.DdlRsvTaskQuery(
                        'maya-look-preview-export', rsv_task_properties
                    )
                    #
                    maya_look_preview_export = ddl_methods.RsvTaskHookExecutor(
                        method_option=maya_look_export_query.get_method_option(),
                        script_option=maya_look_export_query.get_script_option(
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
                    # maya-scene
                    ddl_objects.DdlRsvTaskQuery(
                        'maya-scene-export', rsv_task_properties
                    ).get_method_option(),
                    # maya-look-export
                    ddl_objects.DdlRsvTaskQuery(
                        'maya-look-export', rsv_task_properties
                    ).get_method_option(),
                ]
            )
        )
        maya_proxy_export.execute_with_deadline()
