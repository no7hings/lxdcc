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
            import lxmaya.startup as mya_startup

            mya_startup.MenuSetup().set_setup()
            print 'lx-dcc menu setup: is completed'

        import lxmaya.core as mya_core

        if mya_core.MyaUtil.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from maya import cmds

            cmds.evalDeferred(fnc_)

    @classmethod
    def setup_arnold(cls):
        def fnc_():
            print 'lx-arnold setup: is started'
            import lxarnold.startup as and_startup

            and_startup.MayaSetup().run()
            print 'lx-arnold setup: is completed'

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def setup_usd(cls):
        def fnc_():
            print 'lx-usd setup: is started'
            import lxusd.startup as usd_startup

            usd_startup.UsdSetup.build_environ()
            print 'lx-usd setup: is completed'

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def setup_workspace_environment(cls):
        def fnc_():
            import lxmaya.core as mya_core

            import lxmaya.scripts as mya_scripts

            _fnc = mya_scripts.ScpCbkEnvironment().execute
            mya_core.CallbackOpt(_fnc, 'NewSceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneSaved').register()
            cmds.evalDeferred(_fnc)

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def setup_workspace_gui(cls):
        def fnc_():
            import lxbasic.dcc.scripts as bsd_dcc_scripts

            _fnc = bsd_dcc_scripts.ScpCbkGui().execute
            mya_core.CallbackOpt(_fnc, 'NewSceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneSaved').register()

        import lxmaya.core as mya_core

        if mya_core.MyaUtil.get_is_ui_mode():
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
        print '*'*40


if __name__ == '__main__':
    Setup.run()
