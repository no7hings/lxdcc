# coding:utf-8
import os

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

c = bsc_objects.Configure(
    value='/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/_Wsp/Resource.yml'
)
c.set('option.root', '/rootNode')
c.set('option.path', '/rootNode/Group')
c.set_flatten()
print c


