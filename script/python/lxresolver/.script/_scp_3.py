# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxutil.scripts as utl_scripts

    r = rsv_commands.get_resolver()

    rsv_entity = r.get_rsv_resource(
        project='shl', asset='shengbei'
    )

    rsv_task = rsv_entity.get_rsv_task(step='srf', task='surfacing')

    scene_src_file_path = rsv_task.get_rsv_unit(
        keyword='asset-maya-scene-src-file'
    ).get_result()

    task_properties = r.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)

    scene_src_info_file_path = rsv_task.get_rsv_unit(
        keyword='asset-maya-scene-src-info-file', version=task_properties.get('version')
    ).get_result()

    m = utl_scripts.DotMaFileReader(scene_src_file_path)

    info = m.get_mesh_info(root='/master')

    f = utl_dcc_objects.OsYamlFile(scene_src_info_file_path)

    f.set_write(info)

