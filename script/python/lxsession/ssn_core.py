# coding:utf-8
from lxutil import utl_configure


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


if __name__ == '__main__':
    print HookEngineMtd.get_command(
        'python'
    )
