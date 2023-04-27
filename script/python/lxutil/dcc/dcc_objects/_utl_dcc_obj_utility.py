# coding:utf-8
from lxutil import utl_abstract

from lxutil_gui import utl_gui_core

import lxuniverse.abstracts as unr_abstracts


class Obj(
    utl_abstract.AbsDccObjDef,
    unr_abstracts.AbsObjDagDef,
    unr_abstracts.AbsObjGuiDef
):
    PATHSEP = '/'
    def __init__(self, path, **kwargs):
        self._set_obj_dag_def_init_(path)
        if self.path.startswith(self.PATHSEP):
            self._name = self.path.split(self.PATHSEP)[-1]
        else:
            self._name = self.path

        if 'icon_name' in kwargs:
            self._icon_file_path = utl_gui_core.RscIconFile.get(kwargs.get('icon_name'))
        else:
            self._icon_file_path = utl_gui_core.RscIconFile.get('obj/object')

        if 'type_name' in kwargs:
            self._type_name = kwargs.get('type_name')
        else:
            self._type_name = 'null'

        self._set_obj_gui_def_init_()
    def get_type_name(self):
        return self._type_name

    @property
    def type(self):
        return self._type_name
    @property
    def icon(self):
        return self._icon_file_path

    def create_dag_fnc(self, path):
        _ = self.__class__(path)
        _._icon_file_path = utl_gui_core.RscIconFile.get('obj/group')
        return _

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
