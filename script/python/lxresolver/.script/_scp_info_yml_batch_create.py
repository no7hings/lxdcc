# coding:utf-8
if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxutil.scripts as utl_scripts

    resolver = rsv_commands.get_resolver()

    rsv_project = resolver.get_rsv_project(project='cjd')

    rsv_entities = rsv_project.get_rsv_resources(branch='asset')

    black_list = []
    white_list = ['nn_gongshifu']
    for rsv_entity in rsv_entities:
        entity_name = rsv_entity.properties.get('asset')
        if entity_name in black_list:
            continue
        if white_list:
            if entity_name not in white_list:
                continue
        #
        for step, task in [
            ('mod', 'modeling'),
            ('srf', 'surfacing'),
            ('rig', 'rigging'),
        ]:
            rsv_step = rsv_entity.get_rsv_step(step=step)
            if rsv_step is not None:
                rsv_task = rsv_step.get_rsv_task(task=task)
                if rsv_task is not None:
                    rsv_scene_file_unit = rsv_task.get_rsv_unit(
                        keyword='asset-maya-scene-file'
                    )
                    scene_file_paths = rsv_scene_file_unit.get_result(version='all')
                    if scene_file_paths:
                        for scene_file_path in scene_file_paths:
                            rsv_scene_file_unit_properties = rsv_scene_file_unit.get_properties_by_result(scene_file_path)
                            #
                            scene_info_file_path = rsv_task.get_rsv_unit(
                                keyword='asset-scene-info-file'
                            ).get_result(version=rsv_scene_file_unit_properties.get('version'))
                            #
                            yml_file = utl_dcc_objects.OsYamlFile(scene_info_file_path)
                            if yml_file.get_is_exists() is True:
                                continue
                            bsc_core.Log.trace_method_result(
                                'file-open',
                                u'file="{}"'.format(scene_file_path)
                            )
                            mesh_info = utl_scripts.DotMaFileReader(scene_file_path).get_mesh_info(
                                root='/master/hi'
                            )
                            yml_file.set_write(mesh_info)
                    else:
                        rsv_scene_src_file_unit = rsv_task.get_rsv_unit(
                            keyword='asset-maya-scene-src-file'
                        )
                        scene_src_file_paths = rsv_scene_src_file_unit.get_result(version='all')
                        for scene_src_file_path in scene_src_file_paths:
                            rsv_scene_src_file_unit_properties = rsv_scene_src_file_unit.get_properties_by_result(scene_src_file_path)
                            #
                            scene_info_file_path = rsv_task.get_rsv_unit(
                                keyword='asset-scene-info-file'
                            ).get_result(version=rsv_scene_src_file_unit_properties.get('version'))
                            #
                            yml_file = utl_dcc_objects.OsYamlFile(scene_info_file_path)
                            if yml_file.get_is_exists() is True:
                                continue
                            bsc_core.Log.trace_method_result(
                                'file-open',
                                u'file="{}"'.format(scene_src_file_path)
                            )
                            mesh_info = utl_scripts.DotMaFileReader(scene_src_file_path).get_mesh_info(
                                root='/master/hi'
                            )
                            yml_file.set_write(mesh_info)


