# coding:utf-8
from ... import utl_abstract

from lxobj import obj_abstract


class Obj(
    utl_abstract.AbsDccObjDef,
    obj_abstract.AbsObjDagDef,
    obj_abstract.AbsObjGuiDef
):
    PATHSEP = '/'
    def __init__(self, path):
        self._set_obj_dag_def_init_(path)
        if self.path.startswith(self.PATHSEP):
            self._name = self.path.split(self.PATHSEP)[-1]
        else:
            self._name = self.path

        self._set_obj_gui_def_init_()
    @property
    def type(self):
        return 'tag'
    @property
    def icon(self):
        from lxutil_gui.qt import utl_gui_qt_core
        return utl_gui_qt_core.QtUtilMtd.get_qt_icon(self.type)

    def _set_dag_create_(self, path):
        pass

    def _get_child_paths_(self, path):
        pass

    def _set_child_create_(self, path):
        pass

