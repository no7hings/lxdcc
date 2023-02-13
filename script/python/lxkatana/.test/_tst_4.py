# coding:utf-8
import lxbasic.objects as bsc_objects

from lxkatana import ktn_configure

p = ktn_configure.Data.LOOK_KATANA_WORKSPACE_CONFIGURE_PATH

print p

c = bsc_objects.Configure(None, p)
c.set_flatten()

print c
