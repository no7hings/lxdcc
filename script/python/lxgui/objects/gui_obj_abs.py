# coding:utf-8
from lxsession.objects import ssn_obj_abs


class AbsRsvPanelSession(ssn_obj_abs.AbsSsnObj):
    RSV_PANEL_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsRsvPanelSession, self).__init__(*args, **kwargs)

    def set_execute(self):
        from lxutil_gui.qt import utl_gui_qt_core
        #
        exists_app = utl_gui_qt_core.QtWidgets.QApplication.instance()
        if exists_app is None:
            import sys
            #
            app = utl_gui_qt_core.QtWidgets.QApplication(sys.argv)
            #
            w = self.RSV_PANEL_CLASS(
                configure=self._configure
            )
            w.set_window_show()
            #
            sys.exit(app.exec_())
        #
        else:
            w = self.RSV_PANEL_CLASS(
                configure=self._configure
            )
            w.set_window_show()
