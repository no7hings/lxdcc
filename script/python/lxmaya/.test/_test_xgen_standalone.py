# coding:utf-8
# run maya as standalone
import maya.standalone; maya.standalone.initialize(name='python')
# add module path
import sys; sys.path.insert(0, '/data/e/myworkspace/td/lynxi/workspace/scheme/linux-x64-maya/maya_default/lynxi/maya/scripts/python')
# run command
from lxutil.dcc.dcc_objects import _utl_dcc_obj_storage

_utl_dcc_obj_storage.SceneFile().set_open('/data/f/groom_test/NN_hair_test_v054.ma')
from lxmaya.dcc.dcc_xgn_objects import _ma_dcc_xgn_obj_utility

reload(_ma_dcc_xgn_obj_utility); s = _ma_dcc_xgn_obj_utility.GroomFnc(); s._test()
