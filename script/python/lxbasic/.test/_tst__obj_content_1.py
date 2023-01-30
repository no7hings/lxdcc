# coding:utf-8
import os

import lxbasic.objects as bsc_objects

# c = bsc_objects.Configure(value='{}.yml'.format(os.path.splitext(__file__)[0]))
c = bsc_objects.Configure(value='/data/e/myworkspace/td/lynxi/script/python/lxkatana/.data/texture-resource-shader-group-configure.yml')
c.set_flatten()
print c


