# coding:utf-8
import collections

import datetime

from lxbasic import bsc_core

from lxutil import utl_core

from lxshotgun import stg_configure, stg_core

import lxbasic.objects as bsc_objects


class StgObjQuery(object):
    def __init__(self, stg_connector, stg_obj):
        self._stg_connector = stg_connector
        self._stg_obj = stg_obj
    @property
    def stg_connector(self):
        return self._stg_connector
    @property
    def shotgun(self):
        return self._stg_connector.shotgun
    #
    @property
    def type(self):
        return self._stg_obj.get('type')
    @property
    def id(self):
        return self._stg_obj.get('id')
    @property
    def stg_obj(self):
        return self._stg_obj

    def get(self, key):
        _ = self.shotgun.find_one(
            entity_type=self.type,
            filters=[
                ['id', 'is', self.id]
            ],
            fields=[key]
        )
        if _:
            return _[key]

    def get_all_keys(self):
        _ = self.shotgun.schema_field_read(
            self.type
        )
        if _:
            return _.keys()
        return []

    def get_all(self):
        _ = self.shotgun.find_one(
            entity_type=self.type,
            filters=[
                ['id', 'is', self.id]
            ],
            fields=self.get_all_keys()
        )
        return _

    def set(self, key, value):
        self.shotgun.update(
            self.type, self.id,
            {key: value}
        )
        utl_core.Log.set_module_result_trace(
            'shotgun property set',
            'type="{}", id="{}", property="{}"'.format(
                self.type,
                self.id,
                key
            )
        )

    def set_update(self, key, value):
        self.set(key, value)

    def set_upload(self, key, value):
        self.shotgun.upload(
            self.type, self.id,
            value,
            field_name=key
        )
        utl_core.Log.set_module_result_trace(
            'shotgun entity upload',
            'type="{}", id="{}", property="{}"'.format(
                self.type,
                self.id,
                key
            )
        )

    def set_stg_obj_append(self, key, stg_obj):
        stg_objs = self.get(key) or []
        ids = []
        for i in stg_objs:
            i_id = i['id']
            ids.append(i_id)
        #
        new_id = stg_obj['id']
        if new_id not in ids:
            stg_objs.append(stg_obj)
            self.set(
                key,
                stg_objs
            )

    def set_stg_obj_extend(self, key, stg_objs):
        [self.set_stg_obj_append(key, i) for i in stg_objs]

    def get_storage_name(self):
        return self.get('tank_name')

    def __str__(self):
        return '{}(type={}, id={})'.format(
            self.__class__.__name__,
            self.type, self.id
        )

    def __repr__(self):
        return self.__str__()


class StgConnector(object):
    STG_OBJ_QUERY_CLS = StgObjQuery
    #
    def __init__(self, **kwargs):
        self._shotgun = stg_core.ShotgunMtd().set_shotgun_instance_create()
    @property
    def shotgun(self):
        return self._shotgun
    @classmethod
    def _get_stg_entity_type_(cls, branch):
        return {
            'asset': 'Asset',
            'shot': 'Shot'
        }[branch]

    def _set_stg_filters_completion_by_tags_(self, filters, **kwargs):
        if 'tags' in kwargs:
            filters.append(
                ['tags', 'in', [self.get_stg_tag(i) for i in kwargs['tags']]]
            )

    def get_stg_entity_scheme(self, stg_type, key):
        _ = self.shotgun.schema_field_read(
            entity_type=stg_type, field_name=key
        )
        if isinstance(_, dict):
            return bsc_objects.Configure(value=_)

    def get_stg_projects(self):
        return self._shotgun.find(
            entity_type=stg_configure.StgType.PROJECT,
            filters=[]
        ) or []

    def get_stg_project_queries(self):
        return [self.STG_OBJ_QUERY_CLS(self, i) for i in self.get_stg_projects()]

    def get_stg_project(self, **kwargs):
        """
        :param kwargs: project=<project-name>
        :return:
        """
        project = kwargs['project']
        return self._shotgun.find_one(
            entity_type=stg_configure.StgType.PROJECT,
            filters=[
                ['name', 'is', project]
            ]
        )

    def get_stg_project_query(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
        :return:
        """
        stg_obj = self.get_stg_project(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)
    # tag/role
    def get_stg_role(self, **kwargs):
        pass
    #
    def get_stg_entity_(self, **kwargs):
        pass

    def get_shotgun_entities(self, shotgun_entity_kwargs):
        list_ = []
        _ = self._shotgun.find(**shotgun_entity_kwargs) or []
        key_pattern = ';'.join(map(lambda x: '{{{}}}'.format(x), shotgun_entity_kwargs.get('fields')))
        for i in _:
            i = {k: (v if v else 'N/a') for k, v in i.items()}
            i_key = key_pattern.format(**i)
            list_.append(i_key.decode('utf-8'))
        return list_

    def get_shotgun_entities_(self, **kwargs):
        list_ = []
        _ = self._shotgun.find(**kwargs) or []
        for i in _:
            i = {k: (v if v else 'N/a') for k, v in i.items()}
            list_.append(i)
        return list_
    # entity
    def get_stg_entity(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            asset=<asset-name>/shot=<shot-name>
        :return:
        """
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        entity_name = kwargs[branch]
        #
        return self._shotgun.find_one(
            entity_type=self._get_stg_entity_type_(branch),
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)],
                ['code', 'is', entity_name]
            ]
        )

    def get_stg_entity_query(self, **kwargs):
        """
        :param kwargs: =StgConnector.get_stg_entity
        :return:
        """
        stg_obj = self.get_stg_entity(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)

    def set_stg_entity_create(self, **kwargs):
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        exists_stg_entity = self.get_stg_entity(**kwargs)
        if exists_stg_entity:
            return exists_stg_entity
        #
        entity_name = kwargs[branch]
        role = kwargs['role']
        #
        _ = self._shotgun.create(
            self._get_stg_entity_type_(branch),
            dict(
                project=self.get_stg_project(**kwargs),
                code=entity_name,
                sg_asset_type=role
            )
        )
        #
        utl_core.Log.set_module_result_trace(
            'shotgun entity create',
            u'stg-{}="{}"'.format(branch, entity_name)
        )
        return _

    def get_stg_entities(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            branch=<branch-name> / role=<role-name> / sequence=<sequence-name>
        :return: list(
        )
        """
        filters = [
            ['project', 'is', self.get_stg_project(**kwargs)],
        ]
        if 'branch' in kwargs:
            branches = [kwargs['branch']]
        else:
            if 'role' in kwargs:
                branches = ['asset']
            elif 'sequence' in kwargs:
                branches = ['shot']
            else:
                branches = ['asset', 'shot']
        #
        if 'role' in kwargs:
            filters.append(
                ['sg_asset_type', 'is', kwargs['role']]
            )
        elif 'sequence' in kwargs:
            filters.append(
                ['sg_sequence', 'is', kwargs['sequence']]
            )
        #
        self._set_stg_filters_completion_by_tags_(filters, **kwargs)
        #
        for i_branch in branches:
            return self._shotgun.find(
                entity_type=self._get_stg_entity_type_(i_branch),
                filters=filters
            )

    def get_stg_entity_queries(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            branch=<branch-name>
        :return: list(
        )
        """
        return [
            self.STG_OBJ_QUERY_CLS(self, i)
            for i in self.get_stg_entities(**kwargs)
        ]
    # step
    def get_stg_steps(self, **kwargs):
        """
        :param kwargs:
            branch=<branch-name>
        :return: [<dict>, ...] or []
        """
        branch = kwargs['branch']
        return self._shotgun.find(
            entity_type='Step',
            filters=[
                ['entity_type', 'is', self._get_stg_entity_type_(branch)]
            ]
        ) or []

    def get_stg_step_queries(self, **kwargs):
        """
        :param kwargs:
            = self.get_stg_steps
        :return:
        """
        return [self.STG_OBJ_QUERY_CLS(self, i) for i in self.get_stg_steps(**kwargs)]

    def get_stg_step(self, **kwargs):
        """
        :param kwargs:
            step=<step-name>
        :return:
        """
        step = kwargs['step']
        return self._shotgun.find_one(
            entity_type='Step',
            filters=[
                ['short_name', 'is', step],
            ]
        )

    def get_stg_step_query(self, **kwargs):
        """
        :param kwargs:
            = self.get_stg_step
        :return:
        """
        stg_obj = self.get_stg_step(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)

    def set_stg_step_create(self, **kwargs):
        pass
    # task
    def get_stg_tasks(self, **kwargs):
        """
        :param kwargs:
            step=<step-name>
        :return:
        """
        return self._shotgun.find(
            entity_type='Task',
            filters=[
                ['entity', 'is', self.get_stg_entity(**kwargs)],
                ['step', 'is', self.get_stg_step(**kwargs)],
            ]
        )

    def get_stg_task_queries(self, **kwargs):
        return [self.STG_OBJ_QUERY_CLS(self, i) for i in self.get_stg_tasks(**kwargs)]

    def get_stg_task(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            asset=<asset-name>/shot=<shot-name>
            step=<step-name>
            task=<task-name>
        :return:
        """
        task = kwargs['task']
        return self._shotgun.find_one(
            entity_type='Task',
            filters=[
                ['entity', 'is', self.get_stg_entity(**kwargs)],
                ['step', 'is', self.get_stg_step(**kwargs)],
                ['content', 'is', task],
            ]
        )

    def get_stg_task_query(self, **kwargs):
        stg_obj = self.get_stg_task(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)

    def set_stg_task_create(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            asset=<asset-name>/shot=<shot-name>
            step=<step-name>
            task=<task-name>
        :return:
        """
        #
        exists_stg_task = self.get_stg_task(**kwargs)
        if exists_stg_task:
            return exists_stg_task
        #
        task = kwargs['task']
        _ = self._shotgun.create(
            'Task',
            dict(
                project=self.get_stg_project(**kwargs),
                entity=self.get_stg_entity(**kwargs),
                step=self.get_stg_step(**kwargs),
                content=task
            )
        )
        utl_core.Log.set_module_result_trace(
            'shotgun entity create',
            u'task="{}"'.format(task)
        )
        return _
    # user
    def get_stg_user(self, **kwargs):
        if 'id' in kwargs:
            return self._shotgun.find_one(
                entity_type='HumanUser',
                filters=[
                    ['id', 'is', kwargs['id']]
                ]
            )
        elif 'name' in kwargs:
            return self._shotgun.find_one(
                entity_type='HumanUser',
                filters=[
                    ['name', 'is', kwargs['name']]
                ]
            )
        elif 'user' in kwargs:
            return self._shotgun.find_one(
                entity_type='HumanUser',
                filters=[
                    ['login', 'is', kwargs['user']]
                ]
            )
        elif 'sg_nickname' in kwargs:
            return self._shotgun.find_one(
                entity_type='HumanUser',
                filters=[
                    ['sg_nickname', 'is', kwargs['sg_nickname']]
                ]
            )

    def get_stg_user_query(self, **kwargs):
        stg_obj = self.get_stg_user(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)

    def get_stg_users(self, **kwargs):
        if 'id' in kwargs:
            return self._shotgun.find(
                entity_type='HumanUser',
                filters=[
                    ['id', 'in', kwargs['id']]
                ]
            )
        elif 'name' in kwargs:
            return self._shotgun.find(
                entity_type='HumanUser',
                filters=[
                    ['name', 'in', kwargs['name']]
                ]
            )
        elif 'user' in kwargs:
            return self._shotgun.find(
                entity_type='HumanUser',
                filters=[
                    ['login', 'in', kwargs['user']]
                ]
            )
        elif 'sg_nickname' in kwargs:
            return self._shotgun.find(
                entity_type='HumanUser',
                filters=[
                    ['sg_nickname', 'in', kwargs['sg_nickname']]
                ]
            )
        return []

    def get_stg_version(self, **kwargs):
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        step = kwargs['step']
        task = kwargs['task']
        version = kwargs['version']
        #
        version_code = '{}.{}.{}.{}'.format(kwargs[branch], step, task, version)
        #
        _ = self._shotgun.find_one(
            entity_type='Version',
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)],
                ['code', 'is', version_code],
            ]
        )
        return _

    def get_stg_versions(self, **kwargs):
        _ = self._shotgun.find(
            entity_type='Version',
            filters=[
                # {'type': 'Task', 'id': 20007}
                ['sg_task', 'is', self.get_stg_task(**kwargs)],
            ]
        )
        return _

    def get_stg_version_query(self, **kwargs):
        stg_obj = self.get_stg_version(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)

    def set_stg_version_create(self, **kwargs):
        exists_stg_version = self.get_stg_version(**kwargs)
        if exists_stg_version:
            return exists_stg_version
        #
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        step = kwargs['step']
        task = kwargs['task']
        version = kwargs['version']
        #
        name = '{}.{}.{}.{}'.format(kwargs[branch], step, task, version)
        #
        _ = self._shotgun.create(
            'Version',
            dict(
                project=self.get_stg_project(**kwargs),
                entity=self.get_stg_entity(**kwargs),
                sg_task=self.get_stg_task(**kwargs),
                #
                code=name,
                #
                user=self.get_stg_user(**kwargs),
            )
        )
        utl_core.Log.set_module_result_trace(
            'shotgun entity create',
            u'stg-version="{}"'.format(name)
        )
        return _

    def get_stg_published_file_type(self, **kwargs):
        file_type = kwargs['file_type']
        _ = self._shotgun.find_one(
            "PublishedFileType",
            [
                ['code', 'is', file_type]
            ]
        )
        if _:
            return _

    def set_stg_published_file_create(self, **kwargs):
        stg_project = self.get_stg_project(**kwargs)
        stg_entity = self.get_stg_entity(**kwargs)
        stg_task = self.get_stg_task(**kwargs)
        stg_version = self.get_stg_version(**kwargs)
        #
        version = kwargs['version']
        version_number = int(version[1:])
        #
        file_path = kwargs['file']
        file_opt = bsc_core.StgFileOpt(file_path)
        file_name = file_opt.get_name()
        file_ext = file_opt.get_ext()
        if 'file_type' in kwargs:
            file_type = kwargs['file_type']
            stg_file_type = self.get_stg_published_file_type(
                file_type=file_type
            )
        else:
            if file_ext in ['.ma']:
                stg_file_type = self.get_stg_published_file_type(
                    file_type='Maya Ma'
                )
            else:
                raise RuntimeError()
        #
        if file_opt.get_is_file() is True:
            if stg_version:
                _ = self._shotgun.create(
                    'PublishedFile',
                    {
                        "path": {
                            'local_path': file_path,
                            'link_type': 'local',
                            'name': file_name
                        },
                        "name": file_name,
                        "code": file_name,
                        "published_file_type": stg_file_type,
                        "sg_status_list": "pub",
                        "version": stg_version,
                        "task": stg_task,
                        "project": stg_project,
                        "entity": stg_entity,
                        "path_cache": bsc_core.StorageBaseMtd.set_map_to_platform(file_path),
                        "version_number": version_number,
                     }
                )
                utl_core.Log.set_module_result_trace(
                    'shotgun entity create',
                    u'stg-published-file="{}"'.format(file_path)
                )
                return _

    def get_stg_published_file(self, **kwargs):
        pass

    def get_stg_tag(self, tag_name):
        _ = self._shotgun.find_one(
            entity_type='Tag',
            filters=[
                ['name', 'is', tag_name]
            ]
        )
        return _

    def get_stg_tag_force(self, tag_name):
        stg_obj = self.get_stg_tag(tag_name)
        if stg_obj:
            return stg_obj
        return self.set_stg_tag_create(tag_name)

    def set_stg_tag_create(self, tag_name):
        _ = [
            self._shotgun.create(
                'Tag',
                dict(name=tag_name)
            )
        ]
        utl_core.Log.set_module_result_trace(
            'shotgun entity create',
            u'stg-tag="{}"'.format(tag_name)
        )
        return _

    def get_stg_playlist(self, **kwargs):
        _ = self._shotgun.find_one(
            entity_type='Playlist',
            filters=[
                ['code', 'is', kwargs['playlist']],
                ['project', 'is', self.get_stg_project(**kwargs)],
            ]
        )
        return _

    def get_stg_playlist_force(self, **kwargs):
        stg_obj = self.get_stg_playlist(**kwargs)
        if stg_obj:
            return stg_obj
        return self.set_stg_playlist_create(**kwargs)

    def set_stg_playlist_create(self, **kwargs):
        name = kwargs['playlist']
        _ = self._shotgun.create(
            'Playlist',
            dict(
                code=name,
                project=self.get_stg_project(**kwargs)
            )
        )
        utl_core.Log.set_module_result_trace(
            'shotgun entity create',
            u'stg-playlist="{}"'.format(name)
        )
        return _

    def set_stg_version_movie_update(self, stg_version, movie_file_path):
        task_id = stg_version.get('sg_task').get('id')
        #
        self._shotgun.upload(
            'Version', stg_version.get('id'),
            movie_file_path,
            field_name='sg_uploaded_movie'
        )
        # link to Last Version
        self._shotgun.update(
            'Task', task_id,
            {'sg_last_version': stg_version}
        )
        utl_core.Log.set_module_result_trace(
            'stg-version-movie-update',
            u'file="{}"'.format(movie_file_path)
        )
    # look-pass
    def get_stg_look_pass(self, **kwargs):
        look_pass_code = kwargs['look_pass_code']
        return self._shotgun.find_one(
            entity_type='CustomEntity06',
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)],
                ['code', 'is', look_pass_code]
            ]
        )

    def get_stg_look_pass_query(self, **kwargs):
        stg_obj = self.get_stg_look_pass(**kwargs)
        if stg_obj:
            return self.STG_OBJ_QUERY_CLS(self, stg_obj)

    def set_stg_look_pass_create(self, **kwargs):
        stg_project = self.get_stg_project(**kwargs)
        stg_entity = self.get_stg_entity(**kwargs)
        if stg_project and stg_entity:
            look_pass_code = kwargs['look_pass_code']
            _ = [
                self._shotgun.create(
                    'CustomEntity06',
                    dict(
                        project=stg_project,
                        sg_asset=stg_entity,
                        code=look_pass_code,
                    )
                )
            ]
            utl_core.Log.set_module_result_trace(
                'shotgun entity create',
                u'stg-look-pass="{}"'.format(look_pass_code)
            )
            return _

    def get_stg_look_passes(self, **kwargs):
        return self._shotgun.find(
            entity_type='CustomEntity06',
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)]
            ]
        ) or []

    def get_stg_look_pass_queries(self, **kwargs):
        return [self.STG_OBJ_QUERY_CLS(self, i) for i in self.get_stg_look_passes(**kwargs)]

    def get_stg_deadline_render_info_query(self, **kwargs):
        mapper = dict(
            mod='MOD',
            grm='GRM',
            srf='LOOKDEV',
            rig='LOOKDEV',
            ani='ANI',
            cfx='CFX',
            efx='EFX',
            dmt='DMT',
        )
        step = kwargs['step']
        if step in mapper:
            stg_entity = self._shotgun.find_one(
                entity_type='CustomNonProjectEntity01',
                filters=[
                    ['sg_department', 'is', mapper[step]],
                    ['sg_job_type', 'is', 'Render']
                ]
            )
            if stg_entity is not None:
                stg_entity_query = self.STG_OBJ_QUERY_CLS(self, stg_entity)
                return stg_entity_query

    def get_stg_all_version_types(self):
        c = self.get_stg_entity_scheme(
            'Version', 'sg_version_type'
        )
        if c is not None:
            return c.get('sg_version_type.properties.valid_values.value')

    def get_stg_all_version_status(self):
        c = self.get_stg_entity_scheme(
            'Version', 'sg_status_list'
        )
        if c is not None:
            return c.get('sg_status_list.properties.valid_values.value')


if __name__ == '__main__':
    c = StgConnector()
    _ = c.get_stg_playlist(
        playlist='2022-08-23-SRF-Review', project='cgm'
    )
    stg_version_query = c.get_stg_version_query(
        project='cgm', asset='td_test', step='srf', task='surfacing', version='v028'
    )

    stg_version_query.set_stg_obj_extend(
        'playlists', [_]
    )
