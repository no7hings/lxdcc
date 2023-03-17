# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpWspWorkspace(
    'workspace'
).build()