# coding:utf-8


class ScpCbkGui(object):
    def __init__(self):
        pass
    @classmethod
    def refresh_tool_kit(cls):
        from lxutil_gui.qt import gui_qt_core
        w = gui_qt_core.get_session_window_by_name('dcc-tool-panels/gen-tool-kit')
        if w is not None:
            w.refresh_all()
    @classmethod
    def refresh_all(cls):
        cls.refresh_tool_kit()

    def execute(self, *args, **kwargs):
        self.refresh_all()
