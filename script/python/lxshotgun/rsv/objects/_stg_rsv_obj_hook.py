# coding:utf-8
from lxbasic import bsc_core

from lxutil.rsv import utl_rsv_obj_abstract

from lxshotgun.rsv.objects import _stg_rsv_obj_utility


class RsvShotgunHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvShotgunHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_task_create(self):
        from lxutil import utl_core
        #
        import lxshotgun.objects as stg_objects
        #
        kwargs = self._rsv_scene_properties.value
        #
        stg_connector = stg_objects.StgConnector()
        #
        stg_project = stg_connector.get_stg_project(
            **kwargs
        )
        if stg_project is not None:
            stg_entity = stg_connector.get_stg_entity(
                **kwargs
            )
            if stg_entity is None:
                stg_connector.set_stg_entity_create(**kwargs)
            #
            stg_step = stg_connector.get_stg_step(
                **kwargs
            )
            if stg_step is not None:
                stg_task = stg_connector.get_stg_task(
                    **kwargs
                )
                if stg_task is None:
                    stg_connector.set_stg_task_create(
                        **kwargs
                    )
            else:
                utl_core.Log.set_module_error_trace(
                    'shotgun-entity create',
                    'step="{}" is non-exists.'.format(kwargs['step'])
                )
        else:
            utl_core.Log.set_module_error_trace(
                'shotgun-entity create',
                'project="{}" is non-exists.'.format(kwargs['project'])
            )

    def set_version_create(self):
        version = self._rsv_scene_properties.get('version')
        _stg_rsv_obj_utility.RsvStgTaskOpt(self._rsv_task).set_stg_version_create(
            version=version
        )

    def set_version_export(self):
        version = self._rsv_scene_properties.get('version')
        movie_file = self._hook_option_opt.get('movie_file')
        description = self._hook_option_opt.get('description')
        _stg_rsv_obj_utility.RsvStgTaskOpt(self._rsv_task).set_stg_version_create(
            version=version,
            movie_file=movie_file,
            description=description
        )

    def set_link_export(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = '{branch}-version-dir'
            keyword_1 = '{branch}-no-version-dir'
        elif workspace == 'output':
            keyword_0 = '{branch}-output-version-dir'
            keyword_1 = '{branch}-output-no-version-dir'
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

        utl_dcc_objects.OsDirectory_(version_directory_path).set_link_to(
            no_version_directory_path, replace=True
        )

    def set_publish_file_export(self):
        import lxshotgun.objects as stg_objects

        stg_connector = stg_objects.StgConnector()

        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = '{branch}-maya-scene-file'
        elif workspace == 'output':
            keyword_0 = '{branch}-output-maya-scene-file'
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
        print stg_connector.get_stg_entity()

    def set_review_mov_export(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword = 'asset-review-mov-file'
        elif workspace == 'output':
            keyword = 'asset-output-review-mov-file'
        else:
            raise TypeError()
        #
        movie_file_path = self._hook_option_opt.get('movie_file')
        #
        review_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        review_mov_file_path = review_mov_file_rsv_unit.get_result(
            version=version
        )
        if movie_file_path:
            movie_file_opt = bsc_core.StorageFileOpt(movie_file_path)
            if movie_file_opt.get_is_exists() is True:
                movie_file_opt.set_copy_to_file(
                    review_mov_file_path
                )


