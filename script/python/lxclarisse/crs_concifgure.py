# coding:utf-8
import os


class Root(object):
    MAIN = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    DATA = '{}/.data'.format(MAIN)
