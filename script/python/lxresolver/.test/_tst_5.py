# coding:utf-8
from lxresolver import commands

# d = '/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/td_test/nn_gongshifu.srf.td_test.v002/scene/nn_gongshifu.katana'
#
# r = commands.get_resolver()
#
# print r.get_task_properties_by_scene_src_file_path(d)


# d = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/td_test/katana/nn_gongshifu.srf.td_test.v002.katana'
#
# r = commands.get_resolver()
#
# print r.get_task_properties_by_work_scene_src_file_path(d)

d = '/l/prod/shl/publish/shots/c10/c10010/ani/animation/c10010.ani.animation.v009/maya/c10010.ani.animation.v009.ma'

r = commands.get_resolver()

print r.get_task_properties_by_scene_file_path(d)

