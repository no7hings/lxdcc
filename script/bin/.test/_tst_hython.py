# coding:utf-8
import lxhoudini.dcc.dcc_objects as hou_dcc_objects

from lxbasic import bsc_core

temp_geo = hou_dcc_objects.Node('/obj/temp_geo')

hou_temp_geo, _ = temp_geo.get_dcc_instance('geo')

temp_hda = hou_dcc_objects.Node('/obj/temp_geo/temp_hda')

hou_temp_hda, _ = temp_hda.get_dcc_instance('hashuv')

temp_hda.get_port('usdfile').set(
    '/home/dongchangbao/.lynxi/temporary/2021_0903/test.usd'
)

temp_hda.get_port('outUsdFile').set(
    '/home/dongchangbao/.lynxi/temporary/2021_0903/test-out-0.usd'
)

temp_hda.get_port('execute').hou_port.pressButton()

hou_dcc_objects.Scene.set_file_save_to(
    '/data/f/hython-test/test_0.hip'
)
