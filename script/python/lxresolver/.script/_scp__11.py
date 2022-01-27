# coding:utf-8
import lxbasic.objects as bsc_objects

f = '/data/f'

c = bsc_objects.Configure(value='/l/prod/cjd/publish/assets/chr/didi/srf/srf_anishading/didi.srf.srf_anishading.v001/look/yml/didi.yml')

# print c

for i in c.get_keys('transform.|master|hi|M_body_higrp|*.properties'):
    print i
    # print c.get(i)
