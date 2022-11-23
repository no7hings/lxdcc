# coding:utf-8
import os


class Root(object):
    MAIN = os.path.dirname(__file__.replace('\\', '/'))
    DATA = '{}/.data'.format(MAIN)


class DataFile(object):
    LIBRARY_BASIC = '{}/dtb-library-basic.yml'.format(Root.DATA)
