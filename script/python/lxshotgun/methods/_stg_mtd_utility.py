# coding:utf-8
import copy

from lxutil import utl_configure, utl_core

import lxresolver.commands as rsv_commands

import lxshotgun.objects as stg_objects

import lxresolver.methods as rsv_methods


class StgTaskMtd(object):
    SHOTGUN_TEMPLATE_CONFIGURE = utl_configure.MainData.get_as_configure(
        'shotgun/template'
    )
    @classmethod
    def set_entities_create_by_template(cls, project, entities, task_template):
        stg_connector = stg_objects.StgConnector()
        entity_key = cls.SHOTGUN_TEMPLATE_CONFIGURE.get('task-templates.{}.entity-key'.format(task_template))
        if entities:
            gp = utl_core.GuiProgressesRunner(maximum=len(entities))
            entity_kwargs = dict(
                project=project
            )
            for entity in entities:
                gp.set_update()
                branch, tag = entity_key.split('/')
                i_entity_kwargs = copy.copy(entity_kwargs)
                if branch == 'asset':
                    i_entity_kwargs['role'] = tag
                    i_entity_kwargs['asset'] = entity
                elif branch == 'shot':
                    i_entity_kwargs['sequence'] = entity[:3]
                    i_entity_kwargs['shot'] = entity
                #
                stg_connector.set_stg_entity_create(
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
                        stg_connector.set_stg_task_create(
                            **i_task_kwargs
                        )
                        #
                        rsv_methods.RsvPermissionMtd.set_entity_task_create(
                            **i_task_kwargs
                        )
                    #
                    # cls.set_entity_directories_create(**i_entity_kwargs)
                    #
            #
            gp.set_stop()
    @classmethod
    def set_create_by_rsv_entity(cls, rsv_entity):
        stg_connector = stg_objects.StgConnector()
        #
        rsv_entity_properties = rsv_entity.properties
        branch = rsv_entity_properties.get('branch')
        if branch == 'asset':
            entity_kwargs = rsv_entity_properties.value
            stg_connector.set_stg_entity_create(
                **entity_kwargs
            )
            role = rsv_entity_properties.get('role')
            template = role
            task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
                'task-templates.{}.task-keys'.format(template)
            )
            if task_keys is None:
                task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
                    'task-templates.default.task-keys'
                )
            #
            if task_keys:
                for i_task_key in task_keys:
                    i_task_kwargs = copy.copy(rsv_entity_properties.value)
                    i_step, i_task = i_task_key.split('/')
                    i_task_kwargs['step'] = i_step
                    i_task_kwargs['task'] = i_task
                    #
                    stg_connector.set_stg_task_create(
                        **i_task_kwargs
                    )
            #
            cls.set_entity_directories_create(**entity_kwargs)
    @classmethod
    def set_asset_create(cls, project, asset, role):
        entity_kwargs = dict(
            project=project,
            role=role,
            asset=asset
        )
        stg_connector = stg_objects.StgConnector()
        #
        stg_connector.set_stg_entity_create(
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
                stg_connector.set_stg_task_create(
                    **i_task_kwargs
                )
                #
                rsv_methods.RsvPermissionMtd.set_entity_task_create(
                    **i_task_kwargs
                )
        #
        # cls.set_entity_directories_create(**entity_kwargs)
    @classmethod
    def set_entities_create_by_template_(cls, project, entity_keys, task_template):
        pass
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
        stg_connector = stg_objects.StgConnector()
        stg_entity = stg_connector.get_stg_entity(**kwargs)
        s = stg_api.Sgtk(project_directory_path)
        #
        s.create_filesystem_structure(
            stg_entity['type'], stg_entity['id']
        )


if __name__ == '__main__':
    import lxmaya

    lxmaya.set_reload()

    import lxshotgun.methods as stg_methods

    stg_methods.StgTaskMtd.set_entities_create_by_template(
        project='lib',
        entities=[
            'ast_cg7_dad',
        ],
        task_template='chr'
    )
    #
    if __name__ == '__main__':
        import lxmaya

        lxmaya.set_reload()

        import lxshotgun.methods as stg_methods

        stg_methods.StgTaskMtd.set_entity_directories_create(
            project='cjd',
            asset='qunzhongnan_c'
        )
