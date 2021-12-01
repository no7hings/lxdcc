# coding:utf-8
from lxutil import objects

from lxkatana import ktn_configure

p = ktn_configure.Data.LOOK_KATANA_WORKSPACE_CONFIGURE_PATH

print p

c = objects.Configure(None, p)
c.set_flatten()

print c
