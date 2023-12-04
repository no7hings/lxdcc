# coding:utf-8


def set_scene_mesh_info_match(file_path_0, file_path_1):
    import lxcontent.core as ctt_core
    #
    f_0 = ctt_core.Content(value=file_path_0)
    f_1 = ctt_core.Content(value=file_path_1)
    #
    keys = ['face-vertices', 'point']
    for key in keys:
        f_0_key_paths = f_0.get_keys(regex='mesh.*.{}-uuid'.format(key))
        f_1_key_paths = f_1.get_keys(regex='mesh.*.{}-uuid'.format(key))
        additions = []
        deletions = []
        intersections = []
        for f_key_path in f_0_key_paths:
            obj_path = f_key_path.split('.')[1]
            if f_key_path in f_1_key_paths:
                f_0_value = f_0.get(f_key_path)
                f_1_value = f_1.get(f_key_path)
                if f_0_value != f_1_value:
                    intersections.append(obj_path)
            else:
                deletions.append(obj_path)
        #
        for f_key_path in f_1_key_paths:
            if f_key_path not in f_0_key_paths:
                obj_path = f_key_path.split('.')[1]
                additions.append(obj_path)
        #
        if intersections:
            print '{} changed:'.format(key)
            for i in intersections:
                print i
        #
        if deletions:
            print 'deletions:'
            for i in deletions:
                print i
        #
        if additions:
            print 'additions:'
            for i in additions:
                print i


if __name__ == '__main__':
    set_scene_mesh_info_match(
        file_path_0='/l/prod/shl/publish/assets/chr/nn_gongshifu/mod/modeling/nn_gongshifu.mod.modeling.v008/metadata/nn_gongshifu.info.yml',
        file_path_1='/l/prod/shl/publish/assets/chr/nn_gongshifu/rig/rigging/nn_gongshifu.rig.rigging.v017/metadata/nn_gongshifu.info.yml',
    )
