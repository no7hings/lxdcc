# coding:utf-8
# noinspection PyUnresolvedReferences
from Katana import Callbacks


class Setup(object):
    @classmethod
    def set_menu_setup(cls):
        print 'lx-katana-menu-setup: start'
        from lxkatana import ktn_setup
        ktn_setup.KatanaMenuSetup().set_setup()
        print 'lx-katana-menu-setup: complete'
    @classmethod
    def set_run(cls, *args, **kwargs):
        print '*'*40
        print 'lx-katana-setup: start'
        cls.set_menu_setup()
        print 'lx-katana-setup: complete'
        print '*' * 40


Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=Setup.set_run
)
