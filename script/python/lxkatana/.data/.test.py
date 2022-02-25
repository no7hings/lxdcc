# coding:utf-8
import lxbasic.objects as bsc_objects

c = bsc_objects.Configure(
    value='/data/e/myworkspace/td/lynxi/script/python/lxkatana/.data/look-katana-workspace-configure.yml'
)

c.set_flatten()

print c
