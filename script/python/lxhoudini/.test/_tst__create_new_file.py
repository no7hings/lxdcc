# coding:utf-8
import lxhoudini; lxhoudini.set_reload();

import lxhoudini.dcc.dcc_objects as hou_dcc_objects

f = '/l/prod/cjd/work/shots/z10/z10090/efx/effects/houdini/z10090.efx.effects.v001.hip'

import hou

cmd = "set -g {0}={1}".format('$HIP', '/l/prod/cjd/work/shots/z10/z10090/efx/effects/houdini')
hou.hscript(cmd)

hou_dcc_objects.Scene.new_file_with_dialog(f)