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
            print 'lx-maya-menu-setup: start'
            from lxmaya import ma_setup
            ma_setup.MayaMenuSetup().set_setup()
            print 'lx-maya-menu-setup: complete'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def set_arnold_setup(cls):
        def fnc_():
            print 'lx-arnold-setup: start'
            from lxarnold import and_setup
            and_setup.MayaSetup().run()
            print 'lx-arnold-setup: complete'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def set_run(cls, *args, **kwargs):
        print '*'*40
        print 'lx-maya-setup: start'
        if cls.get_is_maya():
            #
            cls.set_arnold_setup()
            #
            cls.set_menu_setup()
            #
        print 'lx-maya-setup: complete'
        print '*' * 40


if __name__ == '__main__':
    Setup.set_run()
