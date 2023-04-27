# coding:utf-8
from lxbasic import bsc_core

from lxsession import ssn_core

from lxutil.rsv import utl_rsv_obj_abstract

from lxshotgun.rsv.objects import _stg_rsv_obj_utility


class RsvShotgunHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvShotgunHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_task_create(self):
        rsv_task = self._rsv_task
        _stg_rsv_obj_utility.RsvStgTaskOpt(rsv_task).set_stg_task_create()

    def set_qc_task_create(self):
        import copy

        import lxresolver.methods as rsv_methods
        #
        kwargs = self._rsv_scene_properties.value
        step = kwargs['step']
        task = kwargs['task']
        #
        kwargs_qc = copy.copy(kwargs)
        kwargs_qc['step'] = '{}_qc'.format(step)
        kwargs_qc['task'] = '{}_qc'.format(task)
        #
        rsv_task_qc = self._resolver.get_rsv_task(**kwargs_qc)
        if rsv_task_qc is not None:
            pass
        else:
            rsv_methods.RsvPermissionMtd.set_entity_task_create(
                **kwargs_qc
            )
        #
        rsv_task_qc = self._resolver.get_rsv_task(**kwargs_qc)
        _stg_rsv_obj_utility.RsvStgTaskOpt(rsv_task_qc).set_stg_task_create()

    def set_version_create(self):
        rsv_task = self._rsv_task
        version = self._rsv_scene_properties.get('version')
        #
        movie_file = self.get_exists_asset_review_mov_file()
        #
        user = self._hook_option_opt.get('user')
        description = self._hook_option_opt.get('description')
        version_type = self._hook_option_opt.get('version_type')
        notice = None
        version_status = None
        extra_key = self._hook_option_opt.get('extra_key')
        create_shotgun_playlists = self._hook_option_opt.get_as_boolean('create_shotgun_playlists')
        if extra_key:
            extra_data = ssn_core.SsnHookFileMtd.get_extra_data(extra_key)
            if extra_data:
                description = extra_data.get('description')
                notice = extra_data.get('notice')
                #
                version_type = extra_data.get('version_type')
                version_status = extra_data.get('version_status')
        #
        _stg_rsv_obj_utility.RsvStgTaskOpt(rsv_task).set_stg_version_create(
            version=version,
            user=user,
            movie_file=movie_file,
            description=description,
            notice=notice,
            #
            version_type=version_type,
            version_status=version_status,
            #
            create_shotgun_playlists=create_shotgun_playlists
        )

    def set_qc_version_create(self):
        import copy
        #
        kwargs = self._rsv_scene_properties.value
        step = kwargs['step']
        task = kwargs['task']
        #
        kwargs_qc = copy.copy(kwargs)
        kwargs_qc['step'] = '{}_qc'.format(step)
        kwargs_qc['task'] = '{}_qc'.format(task)
        #
        rsv_task_qc = self._resolver.get_rsv_task(**kwargs_qc)
        # to publish
        version_rsv_unit_qc = rsv_task_qc.get_rsv_unit(
            keyword='asset-release-version-dir'
        )
        version_qc = version_rsv_unit_qc.get_new_version()
        #
        version_type = self._hook_option_opt.get('version_type')
        with_qc_review_mov = self._hook_option_opt.get_as_boolean('with_qc_review_mov')
        user = self._hook_option_opt.get('user')
        description = self._hook_option_opt.get('description')
        review_mov_file_path_qc = None
        if with_qc_review_mov is True:
            review_mov_file_path_qc = self.set_qc_review_mov_export(version_qc)
        #
        _stg_rsv_obj_utility.RsvStgTaskOpt(rsv_task_qc).set_stg_version_create(
            version=version_qc,
            version_type=version_type,
            movie_file=review_mov_file_path_qc,
            user=user,
            description=description
        )

    def execute_version_export(self):
        version = self._rsv_scene_properties.get('version')
        movie_file = self.get_exists_asset_review_mov_file()
        description = self._hook_option_opt.get('description')
        _stg_rsv_obj_utility.RsvStgTaskOpt(self._rsv_task).set_stg_version_create(
            version=version,
            movie_file=movie_file,
            description=description
        )

    def execute_link_export(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = '{branch}-release-version-dir'
            keyword_1 = '{branch}-release-no-version-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = '{branch}-temporary-version-dir'
            keyword_1 = '{branch}-temporary-no-version-dir'
        else:
            raise TypeError()
        #
        version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        version_directory_path = version_directory_rsv_unit.get_result(
            version=version
        )
        no_version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        no_version_directory_path = no_version_directory_rsv_unit.get_result(
            version=version
        )

        utl_dcc_objects.OsDirectory_(version_directory_path).link_to(
            no_version_directory_path, replace=True
        )

    def execute_lock_export(self):
        from lxbasic import bsc_core
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = '{branch}-release-version-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = '{branch}-temporary-version-dir'
        else:
            raise TypeError()
        #
        directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        directory_path = directory_rsv_unit.get_result(
            version=version
        )
        bsc_core.StgPathPermissionMtd.lock_all_below(
            directory_path
        )

    def execute_new_registry_json_export(self):
        from lxbasic import bsc_core
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-new-registry-json-file'
            )
            file_path = file_rsv_unit.get_result(version=version)
            raw = dict(
                files=self.get_new_registry_file_data_fnc(
                    self._rsv_task, version
                ),
                info=self.get_new_registry_info_data_fnc(
                    user=self._hook_option_opt.get('user')
                )
            )
            bsc_core.StgFileOpt(file_path).set_write(
                raw
            )
    @classmethod
    def get_new_registry_file_data_fnc(cls, rsv_task, version):
        directory_rsv_unit = rsv_task.get_rsv_unit(
            keyword='{branch}-release-version-dir'
        )
        directory_path = directory_rsv_unit.get_result(
            version=version
        )
        dict_ = {}
        args = [
            '{branch}-maya-scene-src-file',
            '{branch}-maya-scene-file',
            '{branch}-katana-scene-src-file',
            '{branch}-katana-scene-file',
            '{branch}-cache-usd-dir',
            '{branch}-component-usd-file',
            '{branch}-component-registry-usd-file',
            '{branch}-cache-ass-dir',
            '{branch}-look-ass-file',
            '{branch}-look-dir',
            '{branch}-look-klf-file',
        ]
        for i_keyword in args:
            i_keyword = i_keyword.format(
                **rsv_task.properties.get_value()
            )
            i_rsv_unit = rsv_task.get_rsv_unit(
                keyword=i_keyword
            )
            i_result = i_rsv_unit.get_exists_result(version=version)
            if i_result:
                i_roles = i_keyword.split('-')[1:-1]
                i_locations = []
                i_key = i_result[len(directory_path)+1:]
                if i_keyword.endswith('-file'):
                    i_roles.append('file')
                elif i_keyword.endswith('-dir'):
                    i_roles.append('folder')
                dict_[i_key] = dict(
                    roles=i_roles,
                    locations=i_locations
                )
        return dict_
    @classmethod
    def get_new_registry_info_data_fnc(cls, user, time_cost=0):
        return dict(
            date=bsc_core.TimeMtd.get_time(exact=True),
            user=user,
            db_id=69018,
            db_name='production',
            time_cost=time_cost
        )

    def execute_shotgun_file_export(self):
        import lxshotgun.objects as stg_objects
        #
        rsv_scene_properties = self._rsv_scene_properties

        stg_connector = stg_objects.StgConnector()

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = '{branch}-maya-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = '{branch}-temporary-maya-scene-file'
        else:
            raise RuntimeError()
        #
        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(version=version)

        file_properties = scene_file_rsv_unit.get_properties_by_result(scene_file_path)

        stg_connector.set_stg_published_file_create(
            file=scene_file_path, **file_properties.value
        )

    def set_dependency_export(self):
        import lxshotgun.objects as stg_objects
        #
        import lxresolver.commands as rsv_commands
        #
        import lxshotgun.operators as stg_operators
        #
        stg_connector = stg_objects.StgConnector()
        #
        stg_version_query = stg_connector.get_stg_version_query(
            **self._rsv_scene_properties.value
        )
        #
        stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)

        resolver = rsv_commands.get_resolver()
        #
        project = self._rsv_scene_properties.get('project')
        branch = self._rsv_scene_properties.get('branch')
        if branch == 'asset':
            asset = self._rsv_scene_properties.get('asset')
            rsv_model_task = resolver.get_rsv_task(
                project=project,
                asset=asset,
                step='mod',
                task='modeling'
            )
            model_geometry_usd_hi_file_rsv_unit = rsv_model_task.get_rsv_unit(
                keyword='asset-geometry-usd-hi-file'
            )
            model_geometry_usd_hi_file_path = model_geometry_usd_hi_file_rsv_unit.get_result(version='latest')
            if model_geometry_usd_hi_file_path:
                file_properties = model_geometry_usd_hi_file_rsv_unit.get_properties_by_result(model_geometry_usd_hi_file_path)
                stg_model_version = stg_connector.get_stg_version(**file_properties.value)
                stg_version_opt.set_link_model_version(
                    stg_model_version
                )
    @classmethod
    def get_deadline_job_info(cls, step):
        from lxutil import utl_core
        #
        import lxshotgun.objects as stg_objects
        #
        stg_connector = stg_objects.StgConnector()
        print stg_connector.get_stg_resource()

    def set_review_mov_export(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-review-mov-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-review-mov-file'
        else:
            raise TypeError()
        #
        mov_file_path = self._hook_option_opt.get('movie_file')
        if mov_file_path:
            mov_file_opt = bsc_core.StgFileOpt(mov_file_path)
            if mov_file_opt.get_is_exists() is True:
                review_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword
                )
                review_mov_file_path = review_mov_file_rsv_unit.get_result(
                    version=version
                )
                mov_file_opt.set_copy_to_file(
                    review_mov_file_path
                )

    def set_validation_info_export(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-validation-info-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-validation-info-file'
        else:
            raise TypeError()
        #
        info_file_path = self._hook_option_opt.get('validation_info_file')
        if info_file_path:
            info_file_opt = bsc_core.StgFileOpt(info_file_path)
            if info_file_opt.get_is_exists() is True:
                validation_info_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword
                )
                validation_info_file_path = validation_info_file_rsv_unit.get_result(
                    version=version
                )
                info_file_opt.set_copy_to_file(
                    validation_info_file_path
                )

    def set_qc_review_mov_export(self, version_qc):
        from lxbasic import bsc_core

        from lxutil import utl_core

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-review-mov-file'
            keyword_1 = 'asset-katana-render-video-all-mov-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-review-mov-file'
            keyword_1 = 'asset-temporary-katana-render-video-all-mov-file'
        else:
            raise TypeError()

        import copy
        #
        kwargs = self._rsv_scene_properties.value
        step = kwargs['step']
        task = kwargs['task']
        #
        kwargs_qc = copy.copy(kwargs)
        kwargs_qc['step'] = '{}_qc'.format(step)
        kwargs_qc['task'] = '{}_qc'.format(task)
        #
        rsv_task_qc = self._resolver.get_rsv_task(**kwargs_qc)

        review_mov_file_rsv_unit_qc = rsv_task_qc.get_rsv_unit(
            keyword=keyword_0
        )
        review_katana_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        review_mov_file_path_qc = review_mov_file_rsv_unit_qc.get_result(
            version=version_qc
        )
        review_katana_mov_file_path = review_katana_mov_file_rsv_unit.get_result(
            version=version
        )
        review_katana_mov_file_opt = bsc_core.StgFileOpt(
            review_katana_mov_file_path
        )
        if review_katana_mov_file_opt.get_is_exists() is True:
            review_katana_mov_file_opt.set_copy_to_file(
                review_mov_file_path_qc
            )
            return review_mov_file_path_qc
        else:
            utl_core.Log.set_module_warning_trace(
                u'qc review mov export',
                u'file="{}" is non-exists'.format(review_katana_mov_file_path)
            )

