# coding:utf-8
import os

from lxutil import utl_core


class Root(object):
    MAIN = os.path.dirname(__file__.replace('\\', '/'))
    #
    DATA = '{}/.data'.format(MAIN)
    RESOURCES = '{}/.resources'.format(MAIN)
    #
    HOOKS = '{}/hooks'.format(RESOURCES)
