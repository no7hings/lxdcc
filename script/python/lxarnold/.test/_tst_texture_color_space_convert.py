# coding:utf-8
from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

import os

os.environ['OCIO'] = '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'

from lxarnold import and_core


f = '/data/f/tx_test/Old_Wood_v2_Diffuse-6.jpg'

i_0 = and_core.AndImageOpt('/data/f/tx-convert-test/Old_Wood_v2_Diffuse.exr')

print i_0._info

