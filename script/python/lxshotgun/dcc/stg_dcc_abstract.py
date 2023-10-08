# coding:utf-8
from lxutil import utl_abstract

from lxutil_gui.qt import gui_qt_core


class AbsStgNode(utl_abstract.AbsDccObj):
    @property
    def type(self):
        raise NotImplementedError

    @property
    def icon(self):
        return gui_qt_core.QtUtilMtd.get_qt_icon(self.type)

    def get_is_file_reference(self):
        return False

    def get_is_exists(self):
        return True
