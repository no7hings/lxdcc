# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

d_p = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders'


f = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders/osl_string_to_int.osl'

bsc_core.OslFileMtd.set_compile(
    f
)

# utl_scripts.ScpOslFile.set_katana_ui_template_create(
#     f, '/data/f/jinja_test/test.py'
# )
# utl_scripts.ScpOslFile.set_maya_ui_template_create(
#     f, '/data/f/jinja_test/test.py'
# )

# utl_scripts.OslFileMtd.set_compile(
#     '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders/osl_window_box_s.osl'
# )
