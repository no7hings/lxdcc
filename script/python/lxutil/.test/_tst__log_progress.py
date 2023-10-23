# coding:utf-8
import lxbasic.core as bsc_core

import time

c = 10

print '■'

with bsc_core.LogProcessContext.create(maximum=c, label='test', use_as_progress_bar=True) as l_p:
    for i in range(c):
        # time.sleep(1)
        l_p.set_update()

