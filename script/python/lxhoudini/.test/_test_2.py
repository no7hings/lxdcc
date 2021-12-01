# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
reload(utl_dcc_objects)

p = utl_dcc_objects.PyReloader(['lxutil', 'lxhoudini'])

p.set_reload()

from lxhoudini_gui.panel import hou_pnl_widgets

p = hou_pnl_widgets.AttributeConstantTool()

p.set_window_show()
