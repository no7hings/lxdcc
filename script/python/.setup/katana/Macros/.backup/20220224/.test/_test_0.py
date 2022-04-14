# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxkatana import ktn_core

f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/lx_look_pass.yml'

m = ktn_core.NGMacro(
    NodegraphAPI.GetNode('plastic__look')
)

m.set_create_by_configure_file(
    f
)

m.set_create_to_op_script_by_configure_file(f)
