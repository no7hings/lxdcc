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
    def setup_qt_menu(cls):
        def fnc_():
            print 'lx-dcc menu setup: is started'
            from lxmaya import ma_setup
            ma_setup.MenuSetup().set_setup()
            print 'lx-dcc menu setup: is completed'
        from lxmaya import ma_core
        if ma_core.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from maya import cmds
            cmds.evalDeferred(fnc_)
    @classmethod
    def setup_arnold(cls):
        def fnc_():
            print 'lx-arnold setup: is started'
            from lxarnold import and_setup
            and_setup.MayaSetup().run()
            print 'lx-arnold setup: is completed'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def setup_usd(cls):
        def fnc_():
            print 'lx-usd setup: is started'
            from lxusd import usd_setup
            usd_setup.UsdSetup.build_environ()
            print 'lx-usd setup: is completed'
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def setup_workspace_environment(cls):
        def fnc_():
            from lxmaya import ma_core
            import lxmaya.scripts as mya_scripts
            _fnc = mya_scripts.ScpCbkEnvironment().execute
            ma_core.CallbackOpt(_fnc, 'NewSceneOpened').register()
            ma_core.CallbackOpt(_fnc, 'SceneOpened').register()
            ma_core.CallbackOpt(_fnc, 'SceneSaved').register()
            cmds.evalDeferred(_fnc)
        # noinspection PyUnresolvedReferences
        from maya import cmds
        cmds.evalDeferred(fnc_)
    @classmethod
    def setup_workspace_gui(cls):
        def fnc_():
            from lxmaya import ma_core
            import lxutil.scripts as utl_scripts
            _fnc = utl_scripts.ScpCbkGui().execute
            ma_core.CallbackOpt(_fnc, 'NewSceneOpened').register()
            ma_core.CallbackOpt(_fnc, 'SceneOpened').register()
            ma_core.CallbackOpt(_fnc, 'SceneSaved').register()
        #
        from lxmaya import ma_core
        if ma_core.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from maya import cmds
            cmds.evalDeferred(fnc_)
    @classmethod
    def run(cls, *args, **kwargs):
        print '*'*40
        print 'lx-maya setup: is started'
        if cls.get_is_maya():
            cls.setup_arnold()
            cls.setup_usd()
            cls.setup_qt_menu()
            cls.setup_workspace_environment()
            cls.setup_workspace_gui()
            #
        print 'lx-maya setup: is completed'
        print '*' * 40


if __name__ == '__main__':
    Setup.run()
