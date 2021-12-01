# coding:utf-8
if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    from lxutil_gui.panel import utl_pnl_widgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = utl_pnl_widgets.SceneBuildToolPanel()
    #
    w.set_window_show()
    sys.exit(app.exec_())
