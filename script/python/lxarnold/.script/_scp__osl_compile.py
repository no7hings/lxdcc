# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

d_p = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders'

d = utl_dcc_objects.OsDirectory_(d_p)

for i_f_p in d.get_child_file_paths():
    i_f = utl_dcc_objects.OsFile(i_f_p)
    if i_f.ext == '.osl':
        bsc_core.OslFileMtd.set_compile(
            i_f.path
        )
