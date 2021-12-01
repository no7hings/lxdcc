# coding:utf-8
import lxkatana
lxkatana.set_reload()

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

ss = ktn_dcc_objects.AndShaders().get_standard_surfaces()

for i in ss:
    s = ktn_dcc_objects.AndStandardSurface(i.path)
    s.set_port_user_data_float_create('opacity', 'displayOpacity')