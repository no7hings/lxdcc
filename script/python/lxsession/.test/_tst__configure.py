# coding:utf-8
from lxutil import utl_configure

configure = utl_configure.MainData.get_as_configure('hook/engine')

configure.set_flatten()

print configure
