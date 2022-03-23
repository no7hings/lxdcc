# coding:utf-8
from lxutil import utl_core

print utl_core.AppLauncher(
    project='default',
    application='maya'
).get_rez_packages()
