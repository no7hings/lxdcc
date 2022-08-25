# coding:utf-8
from lxutil import utl_abstract

from lxutil_gui import utl_gui_core

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
        from lxutil_gui import utl_gui_core
        return utl_gui_core.RscIconFile.get('node')

    def _set_dag_create_(self, path):
        pass

    def _get_child_paths_(self, path):
        pass

    def _set_child_create_(self, path):
        pass


class Component(utl_abstract.AbsObjGuiDef):
    PATHSEP = '.'
    TYPE_DICT = {
        'f': 'face',
        'e': 'edge',
        'vtx': 'vertex'
    }
    def __init__(self, path):
        self._path = path
        self._name = self._path.split('.')[-1]
        keyword = self.name.split('[')[0]
        self._type = self.TYPE_DICT.get(keyword)
    @property
    def type(self):
        return self._type
    @property
    def name(self):
        return self._name
    @property
    def path(self):
        return self._path
    @property
    def icon(self):
        return utl_gui_core.RscIconFile.get('obj/{}'.format(self.type))

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()
