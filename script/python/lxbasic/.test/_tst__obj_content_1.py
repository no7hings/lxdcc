# coding:utf-8
import os

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

c = bsc_objects.Configure(
    value=bsc_core.CfgFileMtd.get_yaml('katana/workspace/asset-default')
)
c.set_flatten()
print c


