# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts


class MenuSetup(gui_qt_abstracts.AsbGuiQtDccMenuSetup):
    KEY = 'menu setup'

    def __init__(self):
        super(MenuSetup, self).__init__()

    @classmethod
    def get_menu(cls, name):
        qt_menu = gui_qt_core.GuiQtMaya.get_qt_menu(name)
        if qt_menu is not None:
            return qt_menu

        qt_menu_bar = gui_qt_core.GuiQtMaya.get_qt_menu_bar()
        if qt_menu_bar:
            # must set parent
            qt_menu = gui_qt_core.QtWidgets.QMenu(qt_menu_bar)
            qt_menu_bar.addMenu(qt_menu)
            qt_menu.setObjectName(name)
            qt_menu.setTitle(name)
            bsc_core.Log.trace_method_result(
                cls.KEY,
                'add menu: "{}"'.format(name)
            )
            qt_menu.setTearOffEnabled(True)
            return qt_menu

    def set_setup(self):
        with bsc_core.LogContext.create(self.KEY, 'all'):
            import lxsession.commands as ssn_commands
            ssn_commands.set_hook_execute('dcc-menus/gen-menu')
