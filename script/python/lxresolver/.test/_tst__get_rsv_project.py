# coding:utf-8
from lxbasic import bsc_core

import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

# p = r.get_rsv_project(project='cgm')
#
# print p.get_pattern('shot-output-maya-scene-src-file')

f = '/l/prod/cgm/work/shots/z88/z88070/ani/animation/maya/scenes/z88070.ani.animation.v032.ma'

rsv_task = r.get_rsv_task_by_any_file_path(
    f
)

rsv_unit = rsv_task.get_rsv_unit(
    keyword='shot-output-maya-scene-src-file'
)

print rsv_unit.get_result(version='v001')


print bsc_core.SessionYamlMtd.get_key(
    user='leilei003',
    time_tag='2022_0515_1655_46_874629',
)

