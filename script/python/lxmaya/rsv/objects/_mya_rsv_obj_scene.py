# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract

from lxbasic import bsc_core

from lxutil import utl_core

from lxmaya import ma_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.fnc.exporters as mya_fnc_exporters

import lxmaya.fnc.builders as mya_fnc_builders


class RsvDccSceneHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_scene_export(self):
        key = 'asset scene export'
        workspace = self._rsv_scene_properties.get('workspace')
        step = self._rsv_scene_properties.get('step')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        if step in ['cam']:
            location = '/camera_grp'
        else:
            location = root
        #
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to(
            pathsep=pathsep
        ).to_string()
        mya_group = mya_dcc_objects.Group(
            mya_location
        )
        if mya_group.get_is_exists() is True:
            if workspace == 'publish':
                keyword_0 = 'asset-maya-scene-file'
            elif workspace == 'output':
                keyword_0 = 'asset-output-maya-scene-file'
            else:
                raise TypeError()
            #
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            mya_fnc_exporters.SceneExporter(
                option=dict(
                    file=scene_file_path,
                    location=location,
                    #
                    with_xgen_collection=True,
                    with_set=True,
                    #
                    ext_extras=self._hook_option_opt.get('ext_extras', as_array=True)
                )
            ).set_run()
            return scene_file_path
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    key,
                    u'obj="{}" is non-exists'.format(mya_group.path)
                )
            )

    def set_asset_root_property_refresh(self):
        task = self._rsv_scene_properties.get('task')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')

        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            ma_core.CmdObjOpt(mya_root.path).set_customize_attribute_create(
                'pg_{}_version'.format(task),
                version
            )

    def set_asset_camera_scene_src_create(self):
        project = self._rsv_scene_properties.get('project')
        asset = self._rsv_scene_properties.get('asset')
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-maya-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-maya-scene-src-file'
        else:
            raise TypeError()
        #
        orig_file_path = '/l/resource/td/asset/maya/asset-camera.ma'
        orig_file_path = bsc_core.StoragePathMtd.set_map_to_platform(orig_file_path)

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
        orig_file = utl_dcc_objects.OsFile(orig_file_path)
        if orig_file.get_is_exists() is True:
            orig_file.set_copy_to_file(scene_src_file_path, replace=True)
            #
            scene_src_file = utl_dcc_objects.OsFile(scene_src_file_path)
            if scene_src_file.get_is_exists() is True:
                mya_dcc_objects.Scene.set_file_open(scene_src_file_path)
                camera_location = '/camera_grp'
                mya_camera_location = bsc_core.DccPathDagOpt(camera_location).set_translate_to(pathsep).to_string()
                mya_camera_group = mya_dcc_objects.Group(mya_camera_location)
                if mya_camera_group.get_is_exists() is True:
                    mya_fnc_builders.AssetBuilder(
                        option=dict(
                            project=project,
                            asset=asset,
                            #
                            with_model_geometry=True,
                            render_resolution=(2048, 2048),
                        )
                    ).set_run()
                    mya_root = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
                    mya_group = mya_dcc_objects.Group(mya_root)
                    if mya_group.get_is_exists() is True:
                        mya_dcc_objects.Scene.set_current_frame(4)
                        for i in mya_camera_group.get_all_shape_paths(include_obj_type=['camera']):
                            i_camera = mya_dcc_objects.Camera(i)
                            i_camera.set_display_()
                            i_camera.set_frame_to(
                                mya_group.path,
                                percent=.5
                            )
                    else:
                        raise RuntimeError(
                            utl_core.Log.set_module_error_trace(
                                'camera scene create',
                                u'obj="{}" is non-exists'.format(mya_root)
                            )
                        )
                else:
                    raise RuntimeError(
                        utl_core.Log.set_module_error_trace(
                            'camera scene create',
                            u'obj="{}" is non-exists'.format(mya_camera_location)
                        )
                    )
                mya_dcc_objects.Scene.set_file_save()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()

    def set_asset_snapshot_preview_export(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-preview-mov-file'
            keyword_1 = 'asset-review-mov-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-preview-mov-file'
            keyword_1 = 'asset-output-review-mov-file'
        else:
            raise TypeError()

        preview_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        preview_mov_file_path = preview_mov_file_rsv_unit.get_result(
            version=version
        )

        mya_root = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()

        mya_fnc_exporters.PreviewExporter(
            file_path=preview_mov_file_path,
            root=mya_root,
            option=dict(
                use_render=False,
                convert_to_dot_mov=True,
            )
        ).set_run()

        create_review_link = self._hook_option_opt.get('create_review_link') or False
        if create_review_link is True:
            review_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            review_mov_file_path = review_mov_file_rsv_unit.get_result(
                version=version
            )
            preview_mov_file = utl_dcc_objects.OsFile(
                preview_mov_file_path
            )
            review_mov_file = utl_dcc_objects.OsFile(review_mov_file_path)
            if preview_mov_file.get_is_exists() is True:
                if review_mov_file.get_is_exists() is False:
                    preview_mov_file.set_link_to(
                        review_mov_file.path
                    )

    def set_asset_preview_scene_src_create(self):
        project = self._rsv_scene_properties.get('project')
        asset = self._rsv_scene_properties.get('asset')
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-maya-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-maya-scene-src-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                #
                with_model_geometry=True,
                #
                with_surface_look=True,
                with_surface_geometry_uv_map=True,
                #
                geometry_var_names=['hi'],
            )
        ).set_run()
        mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)

    def set_asset_scene_src_create(self):
        project = self._rsv_scene_properties.get('project')
        asset = self._rsv_scene_properties.get('asset')
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-maya-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-maya-scene-src-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)

        with_build = self._hook_option_opt.get_as_boolean('with_build')
        if with_build is True:
            mya_fnc_builders.AssetBuilder(
                option=dict(
                    project=project,
                    asset=asset,
                    #
                    with_model_geometry=self._hook_option_opt.get('with_model_geometry') or False,
                    #
                    with_surface_look=self._hook_option_opt.get('with_surface_look') or False,
                    with_surface_geometry_uv_map=self._hook_option_opt.get('with_surface_geometry_uv_map') or False,
                    #
                    geometry_var_names=self._hook_option_opt.get('geometry_var_names', as_array=True) or [],
                )
            ).set_run()
        #
        mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)

    def set_asset_texture_bake_create(self):
        key = 'asset texture bake create'

        import lxsession.commands as ssn_commands

        option_hook_key = self._hook_option_opt.get('option_hook_key')
        bake_option_hook_key = 'rsv-task-methods/asset/maya/gen-texture-bake'
        bake_convert_option_hook_key = 'rsv-task-methods/asset/maya/gen-texture-bake-convert'

        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')

        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep=pathsep
        )
        mya_group = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_group.get_is_exists() is True:
            bake_resolution = self._hook_option_opt.get('bake_resolution', as_integer=True)
            with_work_scene_src_link = self._hook_option_opt.get('with_work_scene_src_link') or False
            #
            mesh_paths = mya_group.get_all_shape_paths(include_obj_type='mesh')
            bake_option_opt = bsc_core.KeywordArgumentsOpt(
                option=dict(
                    option_hook_key=bake_option_hook_key,
                    #
                    batch_file=self._hook_option_opt.get('batch_file'), file=self._hook_option_opt.get('file'),
                    #
                    user=self._hook_option_opt.get('user'), time_tag=self._hook_option_opt.get('time_tag'),
                    #
                    td_enable=self._hook_option_opt.get('td_enable'), rez_beta=self._hook_option_opt.get('rez_beta'),
                    #
                    bake_location=root,
                    bake_indices=list(range(len(mesh_paths))),
                    bake_resolution=bake_resolution,
                    #
                    dependencies=[option_hook_key],
                )
            )
            bake_session = ssn_commands.set_option_hook_execute_by_deadline(
                bake_option_opt.to_string()
            )
            bake_ddl_job_id = bake_session.get_ddl_job_id()
            if bake_ddl_job_id:
                bake_convert_option_opt = bsc_core.KeywordArgumentsOpt(
                    option=dict(
                        option_hook_key=bake_convert_option_hook_key,
                        #
                        batch_file=self._hook_option_opt.get('batch_file'), file=self._hook_option_opt.get('file'),
                        #
                        user=self._hook_option_opt.get('user'), time_tag=self._hook_option_opt.get('time_tag'),
                        #
                        td_enable=self._hook_option_opt.get('td_enable'), rez_beta=self._hook_option_opt.get('rez_beta'),
                        #
                        with_texture_bake_convert=True,
                        bake_resolution=bake_resolution,
                        with_work_scene_src_link=with_work_scene_src_link,
                        #
                        dependencies=[option_hook_key],
                        #
                        dependent_ddl_job_id_extend=[bake_ddl_job_id]
                    )
                )
                ssn_commands.set_option_hook_execute_by_deadline(
                    bake_convert_option_opt.to_string()
                )
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    key,
                    u'obj="{}" is non-exists'.format(mya_group.path)
                )
            )

    def set_asset_texture_bake(self):
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')

        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep=pathsep
        )
        mya_group = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_group.get_is_exists() is True:
            workspace = self._rsv_scene_properties.get('workspace')
            version = self._rsv_scene_properties.get('version')
            #
            if workspace == 'publish':
                keyword_0 = 'asset-texture-tgt-dir'
            elif workspace == 'output':
                keyword_0 = 'asset-output-texture-tgt-dir'
            else:
                raise RuntimeError()
            #
            texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            texture_tgt_directory_path = texture_tgt_directory_tgt_unit.get_result(
                version=version
            )
            start_index, end_index = self._hook_option_opt.get('start_index'), self._hook_option_opt.get('end_index')
            #
            mesh_paths = mya_group.get_all_shape_paths(include_obj_type='mesh')
            all_indices = list(range(len(mesh_paths)))
            include_indices = all_indices[int(start_index):int(end_index)+1]
            bake_resolution = self._hook_option_opt.get('bake_resolution', as_integer=True)
            #
            mya_fnc_exporters.TextureBaker(
                option=dict(
                    directory=texture_tgt_directory_path,
                    location=root,
                    include_indices=include_indices,
                    resolution=bake_resolution,
                    aa_samples=3
                )
            ).set_run()

    def set_asset_texture_bake_convert(self):
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')

        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep=pathsep
        )
        mya_group = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_group.get_is_exists() is True:
            workspace = self._rsv_scene_properties.get('workspace')
            version = self._rsv_scene_properties.get('version')
            #
            if workspace == 'publish':
                keyword_0 = 'asset-maya-scene-file'
                keyword_1 = 'asset-texture-tgt-dir'
            elif workspace == 'output':
                keyword_0 = 'asset-output-maya-scene-file'
                keyword_1 = 'asset-output-texture-tgt-dir'
            else:
                raise TypeError()
            #
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            #
            texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            texture_tgt_directory_path = texture_tgt_directory_tgt_unit.get_result(
                version=version
            )
            #
            bake_resolution = self._hook_option_opt.get('bake_resolution', as_integer=True)
            #
            mya_fnc_exporters.TextureBaker(
                option=dict(
                    directory=texture_tgt_directory_path,
                    location=root,
                    resolution=bake_resolution,
                )
            ).set_convert_run()
            #
            mya_dcc_objects.Scene.set_file_save_to(
                scene_file_path
            )

    def set_asset_work_scene_src_link(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-maya-scene-file'
            keyword_1 = 'asset-work-maya-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-maya-scene-file'
            keyword_1 = 'asset-work-maya-scene-src-file'
        else:
            raise TypeError()
        #
        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(version=version)

        work_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        latest_work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
            version='latest'
        )
        if latest_work_scene_src_file_path:
            if bsc_core.StorageLinkMtd.get_is_link_source_to(
                    scene_file_path, latest_work_scene_src_file_path
            ) is False:
                new_work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
                    version='new'
                )
                #
                utl_dcc_objects.OsFile(
                    scene_file_path
                ).set_link_to(new_work_scene_src_file_path)
            else:
                utl_core.Log.set_module_warning_trace(
                    'preview work-scene-src link create',
                    u'link="{}" >> "{}" is exists'.format(
                        scene_file_path, latest_work_scene_src_file_path
                    )
                )
        else:
            new_work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
                version='new'
            )
            utl_dcc_objects.OsFile(
                scene_file_path
            ).set_link_to(new_work_scene_src_file_path)


class RsvDccShotSceneHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_scene_open(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        asset_shot = self._hook_option_opt.get('shot')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-shot-maya-scene-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-shot-maya-scene-file'
        else:
            raise TypeError()
        #
        asset_shot_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_file_path = asset_shot_scene_file_rsv_unit.get_exists_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot
            )
        )
        if asset_shot_scene_file_path is not None:
            mya_dcc_objects.Scene.set_file_open(
                asset_shot_scene_file_path
            )
        else:
            raise RuntimeError()

    def set_asset_shot_scene_src_copy(self):
        asset_shot = self._hook_option_opt.get('shot')
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-shot-maya-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-shot-maya-scene-src-file'
        else:
            raise TypeError()
        #
        rsv_project = self._rsv_task.get_rsv_project()
        rsv_shot = rsv_project.get_rsv_entity(
            shot=asset_shot
        )
        #
        shot_scene_file_rsv_unit = rsv_shot.get_available_rsv_unit(
            task=['final_layout', 'animation', 'blocking', 'rough_layout'],
            keyword='shot-maya-scene-file',
        )
        shot_scene_file_path = shot_scene_file_rsv_unit.get_result(
            version='latest',
        )
        #
        asset_shot_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_src_file_path = asset_shot_scene_src_file_rsv_unit.get_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot
            )
        )
        #
        utl_dcc_objects.OsFile(
            shot_scene_file_path
        ).set_copy_to_file(
            asset_shot_scene_src_file_path
        )

    def set_asset_shot_scene_export(self):
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-shot-maya-scene-src-file'
            keyword_1 = 'asset-shot-maya-scene-file'
            keyword_2 = 'asset-maya-scene-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-shot-maya-scene-src-file'
            keyword_1 = 'asset-output-shot-maya-scene-file'
            keyword_2 = 'asset-output-maya-scene-file'
        else:
            raise TypeError()
        #
        asset_shot_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_src_file_path = asset_shot_scene_src_file_rsv_unit.get_exists_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot
            )
        )
        if asset_shot_scene_src_file_path:
            mya_dcc_objects.Scene.set_file_open(asset_shot_scene_src_file_path)
            #
            asset_maya_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_2
            )
            asset_maya_scene_file_path = asset_maya_scene_file_rsv_unit.get_exists_result(
                version=version
            )
            if asset_maya_scene_file_path:
                self._set_shot_asset_rig_replace_(shot_asset, asset_maya_scene_file_path)
            else:
                raise RuntimeError()
            #
            asset_shot_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            asset_shot_scene_file_path = asset_shot_scene_file_rsv_unit.get_result(
                version=version,
                extend_variants=dict(
                    asset_shot=asset_shot
                )
            )
            mya_dcc_objects.Scene.set_file_save_to(
                asset_shot_scene_file_path
            )
        else:
            raise RuntimeError()
    @classmethod
    def _set_shot_asset_rig_replace_(cls, namespace, file_path):
        reference_dict = mya_dcc_objects.References().get_reference_dict_()
        if namespace in reference_dict:
            namespace, root, obj = reference_dict[namespace]
            obj.set_replace(file_path)
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    'usd export',
                    'namespace="{}" is non-exists'.format(namespace)
                )
            )
    # TODO need support for pg_namespace
    @classmethod
    def get_shot_asset_dict(cls):
        dict_ = {}
        r = cls.get_resolver()
        reference_raw = mya_dcc_objects.References().get_reference_raw()
        for i_obj, i_namespace, i_file_path in reference_raw:
            i_rsv_task = r.get_rsv_task_by_any_file_path(
                i_file_path
            )
            i_root = i_obj.get_content_obj_paths()[0]
            if i_rsv_task is not None:
                dict_[i_root] = i_namespace, i_rsv_task
        return dict_
