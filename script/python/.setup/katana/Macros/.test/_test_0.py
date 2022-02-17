# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxkatana import ktn_core

ktn_core.NGMacro(
    NodegraphAPI.GetNode('Group1')
).set_create_by_configure_file(
    '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/lx_render_settings_modifier.yml'
)