# coding:utf-8
import lxshotgun.objects as stg_objects

import lxshotgun.operators as stg_operators

import lxresolver.commands as rsv_commands


class RsvStgProjectOpt(object):
    def __init__(self, rsv_project):
        self._resolver = rsv_commands.get_resolver()
        self._rsv_project = rsv_project
        self._stg_connector = stg_objects.StgConnector()

    def get_default_light_rig_rsv_asset(self):
        _ = self._stg_connector.get_stg_entity_queries(
            project=self._rsv_project.name,
            role='lig',
            tags=['DefaultRig']
        )
        if _:
            return self._rsv_project.get_rsv_entity(
                role='lig',
                asset=_[0].get('code')
            )

    def get_standard_light_rig_rsv_assets(self):
        _ = self._stg_connector.get_stg_entity_queries(
            project=self._rsv_project.name,
            role='lig',
            tags=['StandardRig']
        )
        if _:
            rsv_assets = [
                self._rsv_project.get_rsv_entity(
                    role='lig',
                    asset=i.get('code')
                )
                for i in _
            ]
            default_rsv_asset = self.get_default_light_rig_rsv_asset()
            if default_rsv_asset in rsv_assets:
                rsv_assets.remove(default_rsv_asset)
            #
            rsv_assets.insert(0, default_rsv_asset)
            return rsv_assets
        return []


class RsvStgTaskOpt(object):
    def __init__(self, rsv_task):
        self._rsv_task = rsv_task
        self._stg_connector = stg_objects.StgConnector()

    def set_stg_version_create(self, version, version_type=None, movie_file=None, user=None, description=None):
        branch = self._rsv_task.get('branch')
        stg_version_kwargs = self._rsv_task.properties.copy_value
        stg_version_kwargs['version'] = version
        #
        stg_version_query = self._stg_connector.get_stg_version_query(
            **stg_version_kwargs
        )
        if stg_version_query is None:
            self._stg_connector.set_stg_version_create(
                **stg_version_kwargs
            )
            stg_version_query = self._stg_connector.get_stg_version_query(
                **stg_version_kwargs
            )

        stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)
        #
        version_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='{}-version-dir'.format(branch)
        )
        version_directory_path = version_rsv_unit.get_result(version=version)

        stg_version_opt.set_folder(
            version_directory_path
        )

        if version_type:
            stg_version_opt.set_stg_type(version_type)

        if user:
            stg_user = self._stg_connector.get_stg_user(user=user)
            stg_version_opt.set_stg_user(stg_user)

        if description:
            stg_version_opt.set_description(description)

        if movie_file:
            stg_version_opt.set_movie_upload(
                movie_file
            )

        stg_version_opt = stg_operators.StgVersionOpt(stg_version_query)
        #
        stg_tag = self._stg_connector.get_stg_tag_force('td-batch')
        stg_version_opt.set_stg_tags_append(
            stg_tag
        )
