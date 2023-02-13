# coding:utf-8
from lxutil import utl_core

import time

c = 10

print '■'

with utl_core.LogProgressRunner.create(maximum=c, label='test', use_as_progress_bar=True) as l_p:
    for i in range(c):
        # time.sleep(1)
        l_p.set_update()

