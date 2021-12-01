# coding:utf-8
import os


class Root(object):
    MAIN = os.path.dirname(__file__.replace('\\', '/'))
    #
    DATA = '{}/.data'.format(MAIN)
    RESOURCES = '{}/.resources'.format(MAIN)
    HOOKS = '{}/hooks'.format(RESOURCES)


class Hooks(object):
    ROOT = Root.HOOKS
    @classmethod
    def get_python_file(cls, key):
        return '{}/{}.py'.format(cls.ROOT, key)
