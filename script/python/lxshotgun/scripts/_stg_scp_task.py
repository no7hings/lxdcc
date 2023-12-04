# coding:utf-8
import copy

import lxbasic.core as bsc_core

from lxutil import utl_configure

import lxresolver.commands as rsv_commands

import lxwarp.shotgun.core as wrp_stg_core

import lxresolver.scripts as rsv_scripts


class StgScpTask(object):
    SHOTGUN_TEMPLATE_CONFIGURE = utl_configure.MainData.get_as_configure(
        'shotgun/template'
    )

    @classmethod
    def set_entities_create_by_template(cls, project, entities, task_template):
        stg_connector = wrp_stg_core.StgConnector()
        entity_key = cls.SHOTGUN_TEMPLATE_CONFIGURE.get('task-templates.{}.entity-key'.format(task_template))
        if entities:
            gp = bsc_core.LogProcessContext(maximum=len(entities))
            entity_kwargs = dict(
                project=project
            )
            for entity in entities:
                gp.do_update()
                branch, tag = entity_key.split('/')
                i_entity_kwargs = copy.copy(entity_kwargs)
                if branch == 'asset':
                    i_entity_kwargs['role'] = tag
                    i_entity_kwargs['asset'] = entity
                elif branch == 'shot':
                    i_entity_kwargs['sequence'] = entity[:3]
                    i_entity_kwargs['shot'] = entity
                #
                stg_connector.create_stg_resource(
                    **i_entity_kwargs
                )
                #
                task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
                    'task-templates.{}.task-keys'.format(task_template)
                )
                if task_keys is None:
                    task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
                        'task-templates.default.task-keys'
                    )
                #
                if task_keys:
                    for i_task_key in task_keys:
                        i_task_kwargs = copy.copy(i_entity_kwargs)
                        i_step, i_task = i_task_key.split('/')
                        i_task_kwargs['step'] = i_step
                        i_task_kwargs['task'] = i_task
                        #
                        stg_connector.create_stg_task(
                            **i_task_kwargs
                        )
                        #
                        rsv_scripts.RsvPermissionMtd.set_entity_task_create(
                            **i_task_kwargs
                        )
                    #
                    # cls.set_entity_directories_create(**i_entity_kwargs)
                    #
            #
            gp.set_stop()

    @classmethod
    def set_asset_create(cls, project, asset, role):
        entity_kwargs = dict(
            project=project,
            role=role,
            asset=asset
        )
        stg_connector = wrp_stg_core.StgConnector()
        #
        stg_connector.create_stg_resource(
            **entity_kwargs
        )
        #
        task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
            'task-templates.{}.task-keys'.format(role)
        )
        if task_keys is None:
            task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
                'task-templates.default.task-keys'
            )
        #
        if task_keys:
            for i_task_key in task_keys:
                i_task_kwargs = copy.copy(entity_kwargs)
                i_step, i_task = i_task_key.split('/')
                i_task_kwargs['step'] = i_step
                i_task_kwargs['task'] = i_task
                #
                stg_connector.create_stg_task(
                    **i_task_kwargs
                )
                #
                rsv_scripts.RsvPermissionMtd.set_entity_task_create(
                    **i_task_kwargs
                )
        #
        # cls.set_entity_directories_create(**entity_kwargs)

    @classmethod
    def set_entity_directories_create(cls, **kwargs):
        """
        :param kwargs:
            project:
            asset / shot:
        :return:
        """
        # noinspection PyUnresolvedReferences
        import sgtk.api as stg_api

        #
        r = rsv_commands.get_resolver()
        rsv_project = r.get_rsv_project(**kwargs)
        project_directory_path = rsv_project.get_directory_path()
        stg_connector = wrp_stg_core.StgConnector()
        stg_entity = stg_connector.get_stg_resource(**kwargs)
        s = stg_api.Sgtk(project_directory_path)
        #
        s.create_filesystem_structure(
            stg_entity['type'], stg_entity['id']
        )


if __name__ == '__main__':
    pass