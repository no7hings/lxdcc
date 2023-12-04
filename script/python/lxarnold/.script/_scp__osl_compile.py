# coding:utf-8
from lxutil import utl_core

import lxbasic.core as bsc_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxarnold import and_setup

and_setup.MtoaSetup('/job/PLE/bundle/thirdparty/arnold/6.1.0.1/Linux').set_run()

d_p = '/data/f/osl'

d = utl_dcc_objects.StgDirectory(d_p)

for i_f_p in d.get_child_file_paths():
    i_f = utl_dcc_objects.OsFile(i_f_p)
    if i_f.ext == '.osl':
        bsc_core.OslFileMtd.compile(
            i_f.path
        )
