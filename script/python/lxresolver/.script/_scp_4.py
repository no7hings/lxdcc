# coding:utf-8
if __name__ == '__main__':
    import collections

    from lxbasic import bsc_core

    import lxresolver.commands as rsv_commands

    import lxcontent.objects as ctt_objects

    info = ctt_objects.Configure(value=collections.OrderedDict())

    r = rsv_commands.get_resolver()

    rsv_entity = r.get_rsv_resource(
        project='shl', asset='nn_gongshifu'
    )

    rsv_task = rsv_entity.get_rsv_task(step='mod', task='modeling')

    rsv_scene_info_file_unit = rsv_task.get_rsv_unit(
        keyword='asset-scene-info-file'
    )
    scene_info_file_paths = rsv_scene_info_file_unit.get_result(version='all')

    for scene_info_file_path in scene_info_file_paths:
        rsv_scene_info_file_unit_properties = rsv_scene_info_file_unit.get_properties_by_result(scene_info_file_path)
        sub_key_path = '{asset}.{step}-{task}-{version}'.format(**rsv_scene_info_file_unit_properties.value)
        scene_info = ctt_objects.Configure(value=scene_info_file_path)
        face_vertices_uuid_key_paths = scene_info.get_keys(regex='mesh.*.face-vertices-uuid')
        face_vertices_uuids = [scene_info.get(i) for i in face_vertices_uuid_key_paths]
        #
        all_face_vertices_uuids = bsc_core.HashMtd.get_hash_value(face_vertices_uuids, as_unique_id=True)
        info.set(
            '{}.mesh.face-vertices-uuid'.format(sub_key_path), all_face_vertices_uuids
        )

    print info
