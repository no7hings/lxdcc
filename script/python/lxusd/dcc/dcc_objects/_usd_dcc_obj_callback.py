# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd

from lxusd.dcc.dcc_objects import _usd_dcc_obj_utility

USD_STAGE = Usd.Stage.CreateInMemory()

SCENE = _usd_dcc_obj_utility.Scene()
