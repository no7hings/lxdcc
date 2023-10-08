# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_configure, utl_core

from lxutil_gui.qt import gui_qt_core


class KatanaMenuSetup(gui_qt_core.AsbQtMenuSetup):
    def __init__(self):
        super(KatanaMenuSetup, self).__init__()
    @classmethod
    def get_menu(cls, name):
        qt_menu = gui_qt_core.QtKatanaMtd.get_menu(name)
        if qt_menu is not None:
            return qt_menu
        #
        qt_menu_bar = gui_qt_core.QtKatanaMtd.get_menu_bar()
        if qt_menu_bar:
            # must set parent
            qt_menu = gui_qt_core.QtWidgets.QMenu(qt_menu_bar)
            qt_menu_bar.addMenu(qt_menu)
            qt_menu.setObjectName(name)
            qt_menu.setTitle(name)
            bsc_core.LogMtd.trace_method_result(
                'menu-add',
                u'menu="{}"'.format(name)
            )
            return qt_menu

    def set_setup(self):
        import lxsession.commands as ssn_commands
        ssn_commands.set_hook_execute('dcc-menus/gen-menu')


class KatanaEventSetup(object):
    def __init__(self):
        pass
    @classmethod
    def set_run(cls):
        from lxkatana import ktn_core
        ktn_core.EventMtd.set_events_register()


class KatanaWorkspaceSetup(object):
    def __init__(self):
        pass
    @classmethod
    def add_environment_callback(cls):
        from lxkatana import ktn_core
        #
        import lxkatana.scripts as ktn_scripts
        #
        ktn_core.CallbackMtd.add_as_startup_complete(
            ktn_scripts.ScpCbkEnvironment().execute
        )
        ktn_core.CallbackMtd.add_as_scene_new(
            ktn_scripts.ScpCbkEnvironment().execute
        )
        ktn_core.CallbackMtd.add_as_scene_open(
            ktn_scripts.ScpCbkEnvironment().execute
        )
        ktn_core.CallbackMtd.add_as_scene_save(
            ktn_scripts.ScpCbkEnvironment().execute
        )
    @classmethod
    def add_gui_callback(cls):
        from lxkatana import ktn_core
        if ktn_core.get_is_ui_mode():
            import lxutil.scripts as utl_scripts
            fnc = utl_scripts.ScpCbkGui().execute
            ktn_core.CallbackMtd.add_as_scene_new(fnc)
            ktn_core.CallbackMtd.add_as_scene_open(fnc)
            ktn_core.CallbackMtd.add_as_scene_save(fnc)
    @classmethod
    def set_setup(cls):
        cls.add_environment_callback()
        cls.add_gui_callback()


class KatanaCallbackSetup(object):
    def __init__(self):
        pass
    @classmethod
    def set_run(cls):
        from lxkatana import ktn_core
        #
        ktn_core.CallbackMtd.add_arnold_callbacks()
