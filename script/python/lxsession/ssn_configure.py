# coding:utf-8
import os


class Root(object):
    MAIN = os.path.dirname(__file__.replace('\\', '/'))
    #
    DATA = '{}/.data'.format(MAIN)


class Hook(object):
    HOST = 'localhost'
    PORT = 9527
