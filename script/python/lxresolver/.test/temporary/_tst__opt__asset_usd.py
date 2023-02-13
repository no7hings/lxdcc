# coding:utf-8
import lxresolver.commands as rsv_commands

import lxresolver.operators as rsv_operators

rsv_task_properties = rsv_commands.get_resolver().get_task_properties_by_any_scene_file_path(
    '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/scene/qunzhongnv_b.ma'
)

print rsv_operators.RsvAssetUsdQuery(
    rsv_task_properties
).get_look_properties_file_dict(
    version=rsv_task_properties['version']
)


