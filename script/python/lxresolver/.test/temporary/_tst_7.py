# coding:utf-8
from lxutil import utl_core

import lxresolver.commands as rsv_commands
#
resolver = rsv_commands.get_resolver()

# print rsv_operators.RsvAssetSceneQuery(task_properties).get_maya_src_file(task='surfacing')
# print rsv_operators.RsvAssetSceneQuery(task_properties).get_houdini_src_file()
# print rsv_operators.RsvAssetSceneQuery(task_properties).get_katana_src_file()
# print rsv_operators.RsvAssetTextureQuery(task_properties).get_src_directory()
# print rsv_operators.RsvAssetTextureQuery(task_properties).get_tgt_directory()
# print rsv_operators.RsvAssetLookQuery(task_properties).get_file()

for i in [
    '/l/prod/shl/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v001/maya/td_test.ma',
    'L:/prod/cjd/publish/assets/prp/changting_a/mod/mod_layout/changting_a.mod.mod_layout.v001/maya/changting_a.ma',
    # '/l/prod/cjd/publish/assets/prp/changting_a/mod/mod_layout/changting_a.mod.mod_layout.v001/maya/changting_a.ma',
]:
    file_path = utl_core.Path.map_to_current(i)
    task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=file_path)
    print task_properties

