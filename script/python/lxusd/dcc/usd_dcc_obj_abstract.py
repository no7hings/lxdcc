# coding:utf-8
from lxusd.warp import *

from lxbasic import bsc_core

from lxutil import utl_core

from lxusd import usd_configure

import lxuniverse.configure as unr_configure

import lxuniverse.abstracts as unr_abstracts


class AbsUsdObjScene(unr_abstracts.AbsObjScene):
    FILE_CLS = None
    UNIVERSE_CLS = None

    def __init__(self):
        super(AbsUsdObjScene, self).__init__()
        self._usd_stage = None

    @property
    def usd_stage(self):
        return self._usd_stage

    def restore_all(self):
        self._universe = self.UNIVERSE_CLS()
        self._path_lstrip = None
        #
        self._usd_stage = None

    def set_load_from_file(self, file_path, root=None):
        file_obj = self.FILE_CLS(file_path)
        if file_obj.get_is_exists() is True:
            file_ext = file_obj.ext
            if file_ext in ['.abc']:
                self._set_load_by_dot_abc_(file_obj, root)
            elif file_ext in ['.usd', '.usda']:
                self.load_from_dot_usd_fnc(file_obj, root)

    def set_load_from_dot_abc(self, file_path, root=None):
        file_obj = self.FILE_CLS(file_path)
        self._set_load_by_dot_abc_(file_obj, root)

    def load_from_dot_usd(self, file_path, root=None, location_source=None):
        file_obj = self.FILE_CLS(file_path)
        self.load_from_dot_usd_fnc(file_obj, root, location_source)

    def _set_load_by_dot_abc_(self, file_obj, root=None):
        self.restore_all()
        file_path = file_obj.path
        self._usd_stage = Usd.Stage.CreateInMemory()
        self._root = root
        #
        usd_root = self._usd_stage.GetPseudoRoot()
        if self._root is not None:
            dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(
                self._root, pathsep=usd_configure.Obj.PATHSEP
                )
            if dag_path_comps:
                dag_path_comps.reverse()
            for i in dag_path_comps:
                if i != usd_configure.Obj.PATHSEP:
                    usd_root = self._usd_stage.DefinePrim(i, '')
        #
        usd_root.GetReferences().AddReference(file_path, usd_root.GetPath())
        self._usd_stage.Flatten()
        # base, ext = os.path.splitext(file_path)
        # self._usd_stage.Export('{}.usda'.format(base))

        for i_usd_prim in self._usd_stage.TraverseAll():
            self.node_create_fnc(i_usd_prim)

    def load_from_dot_usd_fnc(self, file_obj, location, location_source):
        self.restore_all()
        file_path = file_obj.path
        self._usd_stage = Usd.Stage.CreateInMemory()
        usd_location = self._usd_stage.GetPseudoRoot()
        if location is not None:
            dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(
                location, pathsep=usd_configure.Obj.PATHSEP
            )
            if dag_path_comps:
                dag_path_comps.reverse()
            #
            for i in dag_path_comps:
                if i != usd_configure.Obj.PATHSEP:
                    usd_location = self._usd_stage.DefinePrim(i, usd_configure.ObjType.Xform)
        #
        reference_location = usd_location.GetPath()
        if location_source is not None:
            reference_location = location_source
        #
        usd_location.GetReferences().AddReference(file_path, reference_location)
        self._usd_stage.Flatten()
        bsc_core.Log.trace_method_result(
            'build universe',
            'file="{}"'.format(file_path)
        )
        with bsc_core.LogProcessContext.create(
                maximum=len([i for i in self._usd_stage.TraverseAll()]), label='build universe'
                ) as l_p:
            for i_usd_prim in self._usd_stage.TraverseAll():
                l_p.set_update()
                self.node_create_fnc(i_usd_prim)

    def node_create_fnc(self, usd_prim):
        obj_category_name = unr_configure.ObjCategory.USD
        obj_type_name = usd_prim.GetTypeName()
        obj_path = usd_prim.GetPath().pathString
        #
        obj_category = self.universe.generate_obj_category(obj_category_name)
        obj_type = obj_category.generate_type(obj_type_name)
        #
        _obj = obj_type.create_obj(obj_path)
        _obj._usd_obj = usd_prim
        if utl_core.get_is_ui_mode() is True:
            import lxgui.qt.core as gui_qt_core

            if obj_type_name == usd_configure.ObjType.Xform:
                _obj.set_gui_attribute('icon', gui_qt_core.GuiQtIcon.generate_by_name('obj/group'))
            elif obj_type_name == usd_configure.ObjType.Mesh:
                _obj.set_gui_attribute('icon', gui_qt_core.GuiQtIcon.generate_by_name('obj/mesh'))
        return _obj
