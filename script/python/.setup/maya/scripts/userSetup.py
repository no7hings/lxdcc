# coding:utf-8
import os


class Setup(object):
    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False
    @classmethod
    def set_menu_setup(cls):
        def fnc_():
            print 'lx-dcc menu setup: is started'
            from lxmaya import ma_setup
            ma_setup.MenuBuilder().set_setup()
            print 'lx-dcc menu setup: is completed'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def set_arnold_setup(cls):
        def fnc_():
            print 'lx-arnold setup: is started'
            from lxarnold import and_setup
            and_setup.MayaSetup().run()
            print 'lx-arnold setup: is completed'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def set_usd_setup(cls):
        def fnc_():
            print 'lx-usd setup: is started'
            from lxusd import usd_setup
            usd_setup.UsdSetup.set_environs_setup()
            print 'lx-usd setup: is completed'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def run(cls, *args, **kwargs):
        print '*'*40
        print 'lx-maya setup: is started'
        if cls.get_is_maya():
            #
            cls.set_arnold_setup()
            #
            cls.set_usd_setup()
            #
            cls.set_menu_setup()
            #
        print 'lx-maya setup: is completed'
        print '*' * 40


if __name__ == '__main__':
    Setup.run()
