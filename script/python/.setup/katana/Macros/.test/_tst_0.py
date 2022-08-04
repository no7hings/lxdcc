# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxkatana import ktn_core

n = NodegraphAPI.GetNode('Group')

f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/lx_asset_loader.yml'

s = NodegraphAPI.GetNode('OpScript')

ktn_core.NGMacro(
    n
).set_create_by_configure_file(
    f
)

ktn_core.NGMacro.set_create_to_op_script_by_configure_file(
    f,
    s
)
