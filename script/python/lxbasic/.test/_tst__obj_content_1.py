# coding:utf-8
import os

from lxbasic import bsc_core

import lxcontent.objects as ctt_objects

c = ctt_objects.Configure(
    value='/data/e/myworkspace/td/lynxi/script/configure/katana/script/macro/workspace.yml'
)
c.set_flatten()
print c
