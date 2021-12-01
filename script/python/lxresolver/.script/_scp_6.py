# coding:utf-8
if __name__ == '__main__':
    import collections

    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxutil.scripts as utl_scripts

    import lxbasic.objects as bsc_objects

    info = bsc_objects.Configure(value=collections.OrderedDict())

    resolver = rsv_commands.get_resolver()

    project = 'shl'

    rsv_project = resolver.get_rsv_project(project=project)

    rsv_entities = rsv_project.get_rsv_entities(branch='asset')

    black_list = ['forest']
    info_file = utl_dcc_objects.OsYamlFile('/l/temp/td/database/{}.info.yml'.format(project))
    for rsv_entity in rsv_entities:
        entity_name = rsv_entity.properties.get('asset')
        if entity_name in black_list:
            continue
        for step, task in [
            ('mod', 'modeling'),
            ('srf', 'surfacing'),
            ('rig', 'rigging')
        ]:
            rsv_step = rsv_entity.get_rsv_step(step=step)
            if rsv_step is not None:
                rsv_task = rsv_step.get_rsv_task(task=task)
                if rsv_task is not None:
                    rsv_scene_info_file_unit = rsv_task.get_rsv_unit(
                        keyword='asset-scene-info-file'
                    )
                    scene_info_file_paths = rsv_scene_info_file_unit.get_result(version='all', trim=[-5, None])
                    for scene_info_file_path in scene_info_file_paths:
                        rsv_scene_info_file_unit_properties = rsv_scene_info_file_unit.get_properties(
                            scene_info_file_path
                        )
                        #
                        sub_key_path = '{asset}.{step}.{task}.{version}'.format(
                            **rsv_scene_info_file_unit_properties.value)
                        scene_info = bsc_objects.Configure(value=scene_info_file_path)
                        #
                        info.set(
                            '{}.file'.format(sub_key_path), scene_info_file_path
                        )
                        #
                        keys = [
                            'face-vertices-uuid',
                            'points-uuid'
                        ]
                        for key in keys:
                            key_paths = scene_info.get_keys(regex='mesh.*.{}'.format(key))
                            #
                            uuids = [scene_info.get(i) for i in key_paths]
                            uuids.sort()
                            #
                            uuids_uuid = bsc_core.HashMtd.get_hash_value(uuids, as_unique_id=True)
                            info.set(
                                '{}.mesh.{}'.format(sub_key_path, key), uuids_uuid
                            )
    #
    info_file.set_write(info.value)
