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


class Hooks(object):
    BRANCH = 'hooks'
    @classmethod
    def get_python_file(cls, key):
        return utl_core.Resources.get(
            '{}/{}.py'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_yaml_file(cls, key):
        return utl_core.Resources.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_command_file(cls, key):
        return utl_core.Resources.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )


class OptionHooks(Hooks):
    BRANCH = 'option-hooks'
