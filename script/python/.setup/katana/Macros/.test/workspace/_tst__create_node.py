# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.scripts as ktn_scripts


for i in [
    'MaterialArea',
    'MaterialAssignArea',
    'PropertiesAssignArea'
]:
    i_f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/_Wsp/{}.yml'.format(i)
    i_m = ktn_scripts.ScpMacro(i_f)
    i_m.build()
    i_m.save()
