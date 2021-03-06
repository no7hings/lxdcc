# coding:utf-8
from lxutil import utl_configure, utl_core

from lxutil_gui.qt import utl_gui_qt_core


class KatanaMenuSetup(utl_gui_qt_core.AsbQtMenuSetup):
    def __init__(self):
        super(KatanaMenuSetup, self).__init__()
    @classmethod
    def get_menu(cls, name):
        qt_menu = utl_gui_qt_core.QtKatanaMtd.get_menu(name)
        if qt_menu is not None:
            return qt_menu
        #
        qt_menu_bar = utl_gui_qt_core.QtKatanaMtd.get_menu_bar()
        if qt_menu_bar:
            # must set parent
            qt_menu = utl_gui_qt_core.QtWidgets.QMenu(qt_menu_bar)
            qt_menu_bar.addMenu(qt_menu)
            qt_menu.setObjectName(name)
            qt_menu.setTitle(name)
            utl_core.Log.set_module_result_trace(
                'menu-add',
                u'menu="{}"'.format(name)
            )
            return qt_menu

    def set_setup(self):
        self.set_menu_build_by_configure(
            utl_configure.MainData.get_as_configure('katana/menu/main')
        )
        #
        import lxsession.commands as ssn_commands
        ssn_commands.set_hook_execute('dcc-menus/gen-menu')


class KatanaEventSetup(object):
    def __init__(self):
        pass
    @classmethod
    def set_run(cls):
        from lxkatana import ktn_core
        ktn_core.EventMethod.set_events_register()


class KatanaCallbackSetup(object):
    def __init__(self):
        pass
    @classmethod
    def set_run(cls):
        from lxkatana import ktn_core
        ktn_core.CallbackMethod.set_callbacks_add()
