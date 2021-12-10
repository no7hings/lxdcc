# coding:utf-8
from lxresolver.objects import rsv_obj_session_abs


class AbsRsvPanelSession(rsv_obj_session_abs.AbsSession):
    RSV_PANEL_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsRsvPanelSession, self).__init__(*args, **kwargs)

    def set_execute(self):
        if self.application in [
            self.Application.Python
        ]:
            import sys
            #
            from PySide2 import QtWidgets
            #
            app = QtWidgets.QApplication(sys.argv)
            #
            w = self.RSV_PANEL_CLASS(
                configure=self._configure
            )
            w.set_window_show()
            #
            sys.exit(app.exec_())
        #
        elif self.application in [
            self.Application.Maya,
            self.Application.Houdini,
            self.Application.Katana,
        ]:
            w = self.RSV_PANEL_CLASS(
                configure=self._configure
            )
            w.set_window_show()
