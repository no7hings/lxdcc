# coding:utf-8
from lxutil import utl_abstract

import lxgui.qt.core as gui_qt_core


class AbsStgNode(utl_abstract.AbsDccObj):
    @property
    def type(self):
        raise NotImplementedError

    @property
    def icon(self):
        return gui_qt_core.GuiQtIcon.generate_by_name(self.type)

    def get_is_file_reference(self):
        return False

    def get_is_exists(self):
        return True
