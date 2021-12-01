# coding:utf-8
from lxutil_prd import utl_prd_objects, utl_prd_commands, utl_prd_core

for i in [
    # '/prod/cg7/work/assets/chr/dad/mod/task_name/maya/scenes/dad.mod.task_name.v001.ma',
    # '/prod/cg7/work/assets/chr/dad/rig/task_name/maya/scenes/dad.rig.task_name.v002.ma',
    # '/prod/cg7/work/assets/chr/dad/grm/task_name/maya/scenes/dad.grm.task_name.v002.ma',
    # '/prod/cg7/work/assets/chr/dad/srf/task_name/maya/scenes/dad.srf.task_name.v002.ma',
    # '/prod/cg7/work/shots/d10/d10010/cfx/task_name/maya/scenes/d10010.cfx.task_name.v002.ma',
    # '/prod/cg7/work/shots/d10/d10010/efx/task_name/maya/scenes/d10010.efx.task_name.v002.ma',
    '/prod/cg7/work/shots/d10/d10010/rlo/task_name/maya/scenes/d10010.rlo.task_name.v002.ma',
    # '/prod/cg7/work/shots/d10/d10010/flo/task_name/maya/scenes/d10010.flo.task_name.v002.ma',
    # '/prod/cg7/work/shots/d10/d10010/lgt/task_name/maya/scenes/dad.lgt.task_name.v002.ma',
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )

    # s._test()

    s.set_load_by_reference_file_paths(
        [
            ('/prod/cg7/publish/assets/cam/camera_rig/rig/rigging/camera_rig.rig.rigging.v001/rig/camera_rig.rig.ma', 'camera_rig'),
            ('/prod/cg7/publish/assets/chr/dragon/rig/layout_rigging/dragon.rig.layout_rigging.v006/rig/dragon.rig.ma', 'dragon'),
            ('/prod/cg7/publish/assets/chr/phoenix/mod/modeling/phoenix.mod.modeling.v004/cache/abc/hi.abc', 'hi'),
        ]
    )
    for j in s.get_objs():
        d = j.get_variant('asset/maya/source/rlt_plf_file_path')
        print j
