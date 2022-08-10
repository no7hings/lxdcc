# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

bsc_core.EnvironMtd.set(
    'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
)

if __name__ == '__main__':
    from lxarnold import and_core
    and_core.AndTextureOpt_.set_color_space_convert_to(
        '/l/prod/cgm/work/assets/chr/bl_duanf_f/srf/surfacing/texture/outsource/v005/bl_duanf_f_body.normal.1001.exr',
        '/data/f/test_maketx/aces/test_0.exr',
        'Utility - Raw',
        'ACES - ACEScg'
    )
