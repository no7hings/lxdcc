# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxkatana import ktn_core

f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/lx_geometry_attributes.yml'

m = ktn_core.NGMacro(
    NodegraphAPI.GetNode('Group')
)

m.set_create_by_configure_file(
    f
)

m.set_create_to_op_script_by_configure_file(
    f
)