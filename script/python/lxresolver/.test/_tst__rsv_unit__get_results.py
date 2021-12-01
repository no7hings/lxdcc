# coding:utf-8
import lxresolver.commands as rsv_commands
#
import lxresolver.operators as rsv_operators
#
scene_file_path = "\l\prod\cjd\publish\assets\prp\cjdj_fengche\rig\rigging\cjdj_fengche.rig.rigging.v003\maya\cjdj_fengche.ma"
# scene_file_path = '/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v051/scene/td_test.ma'
#
#
resolver = rsv_commands.get_resolver()
task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)

print task_properties

print
