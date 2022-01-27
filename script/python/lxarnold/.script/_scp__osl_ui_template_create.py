# coding:utf-8
from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

d_p = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders'

d = utl_dcc_objects.OsDirectory_(d_p)

for i_f_p in d.get_child_file_paths():
    i_f = utl_dcc_objects.OsFile(i_f_p)
    if i_f.ext == '.osl':
        i_katana_o_f_p = '{}/Args/{}.args'.format(d.path, i_f.name_base)
        utl_core.OslShaderMtd.set_katana_ui_template_create(
            i_f.path, i_katana_o_f_p
        )
        i_maya_o_f_p = '{}/maya/ae/ae_{}.py'.format(d.get_parent().path, i_f.name_base)
        utl_core.OslShaderMtd.set_maya_ui_template_create(
            i_f.path, i_maya_o_f_p
        )
