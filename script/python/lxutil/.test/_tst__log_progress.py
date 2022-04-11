# coding:utf-8
from lxutil import utl_core

c = 100

with utl_core.log_progress(maximum=c, label='test', use_as_progress_bar=True) as l_p:
    for i in range(c):
        l_p.set_update()

