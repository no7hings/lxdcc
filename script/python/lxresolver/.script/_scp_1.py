# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxdeadline.methods as ddl_methods

    r = rsv_commands.get_resolver()
    for rsv_entity in r.get_rsv_resources(project='shl', branch='asset', role='flg'):
        rsv_task = rsv_entity.get_rsv_task(step='srf', task='surfacing')
        if rsv_task is not None:
            src_exists_scene_file_path = rsv_task.get_rsv_unit(
                keyword='asset-work-maya-scene-src-file', version='latest'
            ).get_result()
            if src_exists_scene_file_path is not None:
                src_file_obj = utl_dcc_objects.OsFile(src_exists_scene_file_path)
                tgt_exists_scene_file_path = rsv_task.get_rsv_unit(
                    keyword='asset-maya-scene-src-file', version='latest'
                ).get_result()
                if tgt_exists_scene_file_path is not None:
                    tgt_file_obj = utl_dcc_objects.OsFile(tgt_exists_scene_file_path)

                    if src_file_obj.get_timestamp_is_same_to(tgt_file_obj) is False:
                        print src_file_obj, tgt_file_obj

