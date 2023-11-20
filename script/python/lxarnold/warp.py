# coding:utf-8
import pkgutil
import sys

ARNOLD_FLAG = False

__pyarnold = pkgutil.find_loader('arnold')

if __pyarnold:
    ARNOLD_FLAG = True
    # noinspection PyUnresolvedReferences
    import arnold
    ai = sys.modules['arnold']
