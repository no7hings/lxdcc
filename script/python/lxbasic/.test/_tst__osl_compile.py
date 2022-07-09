# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

d_p = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders'


bsc_core.OslShaderMtd.set_compile(
    '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders/osl_window_box_s.osl'
)
