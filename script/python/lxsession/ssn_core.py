# coding:utf-8
from lxutil import utl_configure, utl_core


class HookEngineMtd(object):
    CONFIGURE = utl_configure.MainData.get_as_configure('hook/engine')
    CONFIGURE.set_flatten()
    @classmethod
    def get_all(cls):
        return cls.CONFIGURE.get_branch_keys('command') or []
    @classmethod
    def get_command(cls, hook_engine, **kwargs):
        _ = cls.CONFIGURE.get(
            'command.{}'.format(hook_engine)
        )
        return _.format(**kwargs)


class RscHookFile(object):
    BRANCH = 'hooks'
    @classmethod
    def get_python(cls, key):
        return utl_core.Resources.get(
            '{}/{}.py'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_yaml(cls, key):
        return utl_core.Resources.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_command(cls, key):
        return utl_core.Resources.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_full_key(cls, key):
        return


class RscOptionHookFile(RscHookFile):
    BRANCH = 'option-hooks'


if __name__ == '__main__':
    pass
