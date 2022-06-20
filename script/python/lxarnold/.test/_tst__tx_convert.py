# coding:utf-8
import os

from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

os.environ['OCIO'] = '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'

from lxarnold import and_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

f = '/l/temp/td/dongchangbao/tx_test/new/grandma.z_disp.1026.exr'

t = and_core.AndTextureOpt_(f)

utl_dcc_objects.OsTexture._set_unit_tx_create_by_src_(
    f,
    directory_path='/l/temp/td/dongchangbao/tx_test/new/tx',
    block=True
)
