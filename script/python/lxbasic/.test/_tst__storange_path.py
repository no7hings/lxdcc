# coding:utf-8
from lxbasic import bsc_core

for p_str in [
    '\l\prod\cjd\publish\assets\prp\cjdj_fengche\rig\rigging\cjdj_fengche.rig.rigging.v003\maya\cjdj_fengche.ma',
    'L:\prod\cjd\publish\assets\prp\cjdj_fengche\rig\rigging\cjdj_fengche.rig.rigging.v003\maya\cjdj_fengche.ma'
]:

    print p_str
    #
    print 'orig: ', repr(p_str)

    p = bsc_core.StgPathOpt(p_str)

    print 'current: ', p.path

    print 'current-platform', bsc_core.StorageMtd.set_map_to_platform(
        p.path
    )

    print 'linux', bsc_core.StorageMtd.set_map_to_linux(
        p.path
    )

    print 'windows', bsc_core.StorageMtd.set_map_to_windows(
        p.path
    )

